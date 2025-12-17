<?php
session_start();
require_once 'db_config.php';

// التحقق من أن السائق مسجل دخول
if (!isset($_SESSION['driver_id'])) {
    echo json_encode(['success' => false, 'message' => 'غير مسجل دخول']);
    exit();
}

// الحصول على بيانات الطلب
$action = $_POST['action'] ?? '';
$trip_id = $_POST['trip_id'] ?? 0;

if (empty($action) || empty($trip_id)) {
    echo json_encode(['success' => false, 'message' => 'بيانات غير صحيحة']);
    exit();
}

// معالجة الطلب بناء على الإجراء
if ($action === 'accept') {
    // قبول الرحلة
    $stmt = $conn->prepare("UPDATE trips SET Driver_id = ?, Trip_Status = 'accepted' WHERE Trip_id = ?");
    $stmt->bind_param("ii", $_SESSION['driver_id'], $trip_id);
    
    if ($stmt->execute()) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => 'فشل في تحديث قاعدة البيانات']);
    }
} elseif ($action === 'reject') {
    // رفض الرحلة
    $stmt = $conn->prepare("UPDATE trips SET Trip_Status = 'rejected' WHERE Trip_id = ?");
    $stmt->bind_param("i", $trip_id);
    
    if ($stmt->execute()) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => 'فشل في تحديث قاعدة البيانات']);
    }
} else {
    echo json_encode(['success' => false, 'message' => 'إجراء غير معروف']);
}