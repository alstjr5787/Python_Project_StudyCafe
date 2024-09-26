<?php
include 'dbconfig.php';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die(json_encode(["error" => "연결 실패: " . $conn->connect_error]));
}

$member_id = $_POST['member_id'];
$account_status = $_POST['account_status'];
$suspension_end_date = isset($_POST['suspension_end_date']) ? $_POST['suspension_end_date'] : null;

if ($suspension_end_date === null) {
    $sql = "UPDATE cafe_user SET account_status = ?, suspension_end_date = NULL WHERE member_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $account_status, $member_id);
} else {
    $sql = "UPDATE cafe_user SET account_status = ?, suspension_end_date = ? WHERE member_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("sss", $account_status, $suspension_end_date, $member_id);
}

if ($stmt->execute()) {
    echo json_encode(["success" => "상태가 성공적으로 업데이트되었습니다."]);
} else {
    error_log("SQL Error: " . $stmt->error); 
    echo json_encode(["error" => "상태 업데이트 중: " . $stmt->error]);
}

$stmt->close();
$conn->close();
?>
