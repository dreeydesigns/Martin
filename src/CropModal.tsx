import React, { useState, useRef } from 'react';
import ReactCrop, { Crop, PixelCrop, centerCrop, makeAspectCrop } from 'react-image-crop';
import 'react-image-crop/dist/ReactCrop.css';
import { X, Check } from 'lucide-react';
import { motion } from 'motion/react';

function centerAspectCrop(mediaWidth: number, mediaHeight: number, aspect: number) {
  return centerCrop(
    makeAspectCrop(
      {
        unit: '%',
        width: 90,
      },
      aspect,
      mediaWidth,
      mediaHeight,
    ),
    mediaWidth,
    mediaHeight,
  )
}

interface CropModalProps {
  imageSrc: string;
  aspectRatio: number;
  onClose: () => void;
  onCropComplete: (croppedImageUrl: string) => void;
  isDarkMode: boolean;
}

export default function CropModal({ imageSrc, aspectRatio, onClose, onCropComplete, isDarkMode }: CropModalProps) {
  const [crop, setCrop] = useState<Crop>();
  const [completedCrop, setCompletedCrop] = useState<PixelCrop>();
  const imgRef = useRef<HTMLImageElement>(null);

  const onImageLoad = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const { width, height } = e.currentTarget;
    setCrop(centerAspectCrop(width, height, aspectRatio));
  };

  const getCroppedImg = () => {
    if (!completedCrop || !imgRef.current) {
      return;
    }

    const image = imgRef.current;
    const canvas = document.createElement('canvas');
    const scaleX = image.naturalWidth / image.width;
    const scaleY = image.naturalHeight / image.height;
    
    canvas.width = completedCrop.width;
    canvas.height = completedCrop.height;
    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    ctx.drawImage(
      image,
      completedCrop.x * scaleX,
      completedCrop.y * scaleY,
      completedCrop.width * scaleX,
      completedCrop.height * scaleY,
      0,
      0,
      completedCrop.width,
      completedCrop.height
    );

    const base64Image = canvas.toDataURL('image/jpeg');
    onCropComplete(base64Image);
  };

  const t = {
    bg: isDarkMode ? "bg-zinc-900 border-zinc-800" : "bg-white border-stone-200",
    textPrimary: isDarkMode ? "text-white" : "text-zinc-900",
  };

  return (
    <div className="fixed inset-0 z-[200] bg-black/90 flex flex-col items-center justify-center p-4">
      <div className={`w-full max-w-lg rounded-xl overflow-hidden shadow-2xl border flex flex-col max-h-[90vh] ${t.bg}`}>
        <div className="flex items-center justify-between p-4 border-b border-inherit bg-inherit z-10">
          <h2 className={`text-lg font-medium ${t.textPrimary}`}>Crop Image</h2>
          <button onClick={onClose} className="p-2 rounded-full hover:bg-black/10 transition-colors">
            <X size={20} className={t.textPrimary} />
          </button>
        </div>
        
        <div className="p-4 overflow-y-auto flex items-center justify-center bg-black">
          <ReactCrop
            crop={crop}
            onChange={(_, percentCrop) => setCrop(percentCrop)}
            onComplete={(c) => setCompletedCrop(c)}
            aspect={aspectRatio}
            circularCrop={aspectRatio === 1}
          >
            <img
              ref={imgRef}
              src={imageSrc}
              onLoad={onImageLoad}
              alt="Crop me"
              style={{ maxHeight: '60vh' }}
              crossOrigin="anonymous"
            />
          </ReactCrop>
        </div>

        <div className="p-4 border-t border-inherit bg-inherit flex justify-end gap-3 z-10">
          <button 
            onClick={onClose}
            className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${isDarkMode ? 'border-zinc-700 text-zinc-300 hover:bg-zinc-800' : 'border-stone-300 text-zinc-700 hover:bg-stone-100'}`}
          >
            Cancel
          </button>
          <button 
            onClick={getCroppedImg}
            className="px-4 py-2 flex items-center gap-2 rounded-lg text-sm font-medium bg-[#c5a059] text-white hover:bg-[#b08c4a] transition-colors"
          >
            <Check size={16} /> Apply Crop
          </button>
        </div>
      </div>
    </div>
  );
}
