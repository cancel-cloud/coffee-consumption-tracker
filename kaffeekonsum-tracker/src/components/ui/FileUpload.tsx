import React, { useRef } from "react";

interface FileUploadProps {
  onFileChange: (file: File | null) => void;
  accept?: string;
  label?: string;
}

export default function FileUpload({ onFileChange, accept, label }: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = React.useState<string>("");

  const handleClick = () => {
    inputRef.current?.click();
  };
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setFileName(file ? file.name : "");
    onFileChange(file);
  };

  return (
    <div className="flex items-center gap-2">
      <button type="button" className="border rounded px-3 py-1 bg-accent" onClick={handleClick}>
        {label || "Datei auswählen"}
      </button>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        style={{ display: "none" }}
        onChange={handleChange}
      />
      <span className="text-muted-foreground text-sm">
        {fileName || "Keine Datei ausgewählt"}
      </span>
    </div>
  );
} 