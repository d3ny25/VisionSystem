"""
camera.py — Módulo de Captura de Imágenes

Gestiona la webcam USB con una conexión persistente (el dispositivo no se abre 
y cierra en cada captura) y thread-safe. Incluye warmup de frames para evitar 
capturas oscuras o inestables al inicio.

El módulo redimensiona imágenes a máximo 384×384px y las codifica en Base64
para optimizar el envío al LLM.
"""

import cv2
import base64
import threading
from io import BytesIO
from typing import Optional


class CameraManager:
    """Gestor de cámara persistente y thread-safe."""
    
    def __init__(self, camera_index: int = 1, warmup_frames: int = 5):
        """
        Inicializa el gestor de cámara.
        
        Args:
            camera_index: Índice de la cámara preferida (por defecto 1 para USB)
            warmup_frames: Número de frames para estabilizar la cámara
        """
        self.camera_index = camera_index
        self.fallback_index = 0 if camera_index != 0 else 1
        self.active_camera_index = None
        self.warmup_frames = warmup_frames
        self.cap = None
        self.lock = threading.Lock()
        self._initialize_camera()
    
    def _open_camera(self, index: int, backend: Optional[int] = None):
        """Intenta abrir una cámara con el backend especificado."""
        if backend is not None:
            cap = cv2.VideoCapture(index, backend)
        else:
            cap = cv2.VideoCapture(index)

        if not cap.isOpened():
            cap.release()
            return None

        return cap

    def _probe_camera(self, index: int, backend: Optional[int] = None):
        """Prueba una cámara y devuelve su captura y resolución si funciona."""
        cap = self._open_camera(index, backend)
        if cap is None:
            return None, None

        ret, frame = cap.read()
        if not ret or frame is None:
            cap.release()
            return None, None

        h, w = frame.shape[:2]
        return cap, w * h

    def _find_best_camera(self, max_cameras: int = 5):
        """Busca la cámara disponible con mayor resolución reportada."""
        backend = cv2.CAP_DSHOW if hasattr(cv2, 'CAP_DSHOW') else None
        available = []

        for idx in range(max_cameras):
            cap, resolution = self._probe_camera(idx, backend)
            if cap is None:
                continue
            available.append((resolution, idx, cap))
            print(f"ℹ️ Cámara {idx} detectada - resolución aproximada {resolution} px")

        if not available:
            return None, None

        available.sort(reverse=True, key=lambda item: item[0])
        best_resolution, best_idx, best_cap = available[0]

        for _, idx, cap in available[1:]:
            cap.release()

        print(f"ℹ️ Cámara de mayor resolución encontrada: índice {best_idx} ({best_resolution} px)")
        return best_idx, best_cap

    def _initialize_camera(self):
        """Abre la cámara preferida o detecta la mejor cámara disponible."""
        try:
            backend = cv2.CAP_DSHOW if hasattr(cv2, 'CAP_DSHOW') else None
            self.cap = self._open_camera(self.camera_index, backend)
            if self.cap is not None:
                self.active_camera_index = self.camera_index
            else:
                print(f"⚠️ No se pudo abrir la cámara preferida (índice {self.camera_index}). Buscando la mejor cámara disponible...")
                best_idx, best_cap = self._find_best_camera()
                if best_cap is None:
                    raise RuntimeError(f"No se pudo abrir ninguna cámara (índices intentados: {self.camera_index}, {self.fallback_index})")
                self.cap = best_cap
                self.active_camera_index = best_idx

            # Configurar resolución preferida en la cámara seleccionada
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)

            # Warmup: descartar los primeros frames para estabilidad
            successful_frame = False
            for _ in range(self.warmup_frames):
                ret, _ = self.cap.read()
                if ret:
                    successful_frame = True

            if not successful_frame:
                print(f"⚠️ Advertencia: no se obtuvo un frame estable durante el warmup de la cámara {self.active_camera_index}")

            print(f"📷 Cámara inicializada (índice: {self.active_camera_index})")
        except Exception as e:
            print(f"❌ Error inicializando cámara: {e}")
            self.cap = None
    
    def capture_frame(self) -> Optional:
        """
        Captura un frame crudo de OpenCV.
        
        Returns:
            Frame de OpenCV o None si falla
        """
        with self.lock:
            if self.cap is None:
                return None
            
            ret, frame = self.cap.read()
            if not ret:
                return None
            
            return frame
    
    def frame_to_base64(self, frame, max_size: int = 384) -> str:
        """
        Redimensiona frame a máximo max_size×max_size y codifica en Base64.
        
        Args:
            frame: Frame de OpenCV
            max_size: Dimensión máxima para redimensionamiento
        
        Returns:
            String Base64 de la imagen JPEG
        """
        # Redimensionar manteniendo aspecto
        h, w = frame.shape[:2]
        scale = min(max_size / w, max_size / h)
        new_w, new_h = int(w * scale), int(h * scale)
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # Codificar a JPEG
        _, buffer = cv2.imencode('.jpg', resized, [cv2.IMWRITE_JPEG_QUALITY, 75])
        
        # Convertir a Base64
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        return img_base64
    
    def get_camera_data(self) -> Optional[str]:
        """
        Captura frame y devuelve como Base64 listo para LLM.
        
        Returns:
            String Base64 o None si falla
        """
        frame = self.capture_frame()
        if frame is None:
            print("❌ Fallo al capturar frame")
            return None
        
        try:
            img_base64 = self.frame_to_base64(frame)
            return img_base64
        except Exception as e:
            print(f"❌ Error al codificar imagen: {e}")
            return None
    
    def close(self):
        """Libera la cámara limpiamente."""
        with self.lock:
            if self.cap is not None:
                self.cap.release()
                self.cap = None
                print("📷 Cámara liberada")
