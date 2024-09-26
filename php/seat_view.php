<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT id, start_time, status, scheduled_end_time, user_id FROM cafe_seat";
$result = $conn->query($sql);

$response = array();

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $cafe_seat = array(
            'id' => $row['id'],
            'start_time' => $row['start_time'],
            'status' => $row['status'],
            'scheduled_end_time' => $row['scheduled_end_time'],
            'user_id' => $row['user_id'],
        );
        array_push($response, $cafe_seat);
    }
    
    echo json_encode($response);
    
} else {
    echo "No Seat found";
}

$conn->close();

?>