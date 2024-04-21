import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";

const fileTypes = ["JPG", "PNG"];


function DragDrop() {
  const [file, setFile] = useState(null);
  const handleChange = (file) => {
    setFile(file);
  };
  
  return (
    <FileUploader className="fileuploader" handleChange={handleChange} name="file" types={fileTypes} multiple={false} />
  );
}

export default DragDrop;