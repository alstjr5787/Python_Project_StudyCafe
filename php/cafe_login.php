<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die(json_encode(["error" => "연결 실패: " . $conn->connect_error]));
}

$member_id = $_POST['member_id'];
$member_password = $_POST['member_password'];

$sql = "SELECT * FROM cafe_user WHERE member_id='$member_id'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $hashed_password = $row['member_password'];
    $account_status = $row['account_status'];
    $suspension_end_date = $row['suspension_end_date'];

    if (password_verify($member_password, $hashed_password)) {
        echo json_encode([
            "status" => "success",
            "account_status" => $account_status,
            "suspension_end_date" => $suspension_end_date
        ]);
    } else {
        echo json_encode(["status" => "failure", "message" => "아이디 또는 비밀번호가 잘못되었습니다."]);
    }
} else {
    echo json_encode(["status" => "failure", "message" => "아이디 또는 비밀번호가 잘못되었습니다."]);
}

$conn->close();
?>
