<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$id = $_POST['id'];
$status = $_POST['status'];
$user_id = $_POST['user_id']; 

$current_time = date('Y-m-d H:i:s');

if ($status === 'false') {
    $sql = "UPDATE cafe_seat SET status='$status', start_time='$current_time', scheduled_end_time=NULL, user_id='$user_id' WHERE id='$id'";
} else {
    $scheduled_end_time = date('Y-m-d H:i:s', strtotime($current_time . ' + 2 hours'));
    $sql = "UPDATE cafe_seat SET status='$status', start_time='$current_time', scheduled_end_time='$scheduled_end_time', user_id='$user_id' WHERE id='$id'";
}

if ($conn->query($sql) === TRUE) {
    echo json_encode(array('success' => true));  
} else {
    echo json_encode(array('success' => false, 'error' => $conn->error));  
}

$conn->close();
?>
