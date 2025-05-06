import React, { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
// Required styles for text and annotation layers
import "react-pdf/dist/Page/TextLayer.css";
import "react-pdf/dist/Page/AnnotationLayer.css";

// Point pdfjs to the worker on UNPKG (version is auto-matched)
pdfjs.GlobalWorkerOptions.workerSrc =
    `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

export default function PdfViewer({ src }) {
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);

    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages);
    }

    return (
        <div style={{ width: "100%" }}>
            <div style={{ marginBottom: 8 }}>
                <button
                    onClick={() => setPageNumber(page => Math.max(page - 1, 1))}
                    disabled={pageNumber <= 1}
                >
                    Previous
                </button>
                <button
                    onClick={() =>
                        setPageNumber(page => Math.min(page + 1, numPages || page))
                    }
                    disabled={pageNumber >= (numPages || 1)}
                    style={{ marginLeft: 8 }}
                >
                    Next
                </button>
                <span style={{ marginLeft: 16 }}>
                    Page {pageNumber} of {numPages || "--"}
                </span>
            </div>

            <Document
                file={src}
                onLoadSuccess={onDocumentLoadSuccess}
                loading="Loading PDF..."
            >
                <Page pageNumber={pageNumber} width={800 /* adjust as needed */} />
            </Document>
        </div>
    );
}
