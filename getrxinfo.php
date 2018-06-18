<html>
<head></head>
<body>
<?php

// URLs to get APRS Info from
/* $aprs_status_urls = [
    'http://glidern1.glidernet.org:14501/status.json',
    'http://glidern2.glidernet.org:14501/status.json',
    'http://glidern3.glidernet.org:14501/status.json',
    'http://glidern4.glidernet.org:14501/status.json'
    ]; */

$aprs_status_urls = [
    'http://glidern1.glidernet.org:14501/status.json'];
    
foreach ($aprs_status_urls as $status) {
    $contents = file_get_contents($status); 
    $contents = utf8_encode($contents); 
    $results = json_decode($contents); 
    echo "<h1>URL = $status</h1><br>";
    echo "VARDUMP<br>";
    var_dump($results);
    echo "CONTENT<br>";
    echo "$contents";
}

?>
</body>
</html>
