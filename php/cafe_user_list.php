<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT member_id, name, phone_number, account_status, suspension_end_date FROM cafe_user";
$result = $conn->query($sql);

$response = array();

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $cafe_user = array(
            'member_id' => $row['member_id'],
            'name' => $row['name'],
            'phone_number' => $row['phone_number'],
            'account_status' => $row['account_status'],
            'suspension_end_date' => $row['suspension_end_date'],
        );
        array_push($response, $cafe_user);
    }
    
    echo json_encode($response);
    
} else {
    echo "No User found";
}

$conn->close();

?>