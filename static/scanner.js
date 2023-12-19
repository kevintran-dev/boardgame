function onScanSuccess(decodedText) {
    // Handle the scanned code as you like, for example:

    UPC = decodedText;
    console.log(UPC);
    html5QrcodeScanner.pause();
    UPC_lookup();
}
const formatsToSupport = [
    Html5QrcodeSupportedFormats.QR_CODE,
    Html5QrcodeSupportedFormats.UPC_A,
    Html5QrcodeSupportedFormats.UPC_E,
    Html5QrcodeSupportedFormats.UPC_EAN_EXTENSION,
];

const html5QrcodeScanner = new Html5QrcodeScanner(
    "reader",
    {
        fps: 10,
        qrbox: { width: 250, height: 250 },
        formatsToSupport: formatsToSupport
    },
    /* verbose= */ false);


html5QrcodeScanner.render(onScanSuccess)