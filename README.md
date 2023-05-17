# PDF_


This application returns metadata of a pdf and extracts images from a pdf using Tika library.

Metadata includes,

1) Security properties like: signing- allowed/not, encrypted/not, corrupted/not, content copying- allowed/not etc.,

2) Other properties like: Number of hidden layers, printing-allowed/not etc.,


It highlights all images in pdf and numbers them, then creates a new highlighted pdf and saves it in the path provided.


Tech: Python

libraries used: PyMuPdf, Tika
