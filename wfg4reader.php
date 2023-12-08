<?php

// Read $argv[1] to get the file path
if (!isset($argv[1])) {
    echo "Please specify the file path as the first argument.";
    exit;
}

$filePath = $argv[1];

// Open the file in binary read mode
if ($fp = fopen($filePath, "rb")) {
    // Read the header (7 integers)
    $headerStr = @fread($fp, 8 * 4);
    $header = unpack("l7/f1empty_value", $headerStr);


    // Output the extracted data for testing

    // Read the data (1 integer per byte)
    $dataStr = @fread($fp, 4 * $header[7]);
    $data = unpack("l*", $dataStr);

    // Output the extracted data for testing
    print_r($data);
    print_r($header);

} else {
    echo "Failed to open the file.";
}

?>
