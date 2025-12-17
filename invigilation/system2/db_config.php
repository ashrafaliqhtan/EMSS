<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "system2";

// إنشاء الاتصال
$conn = new mysqli($servername, $username, $password, $dbname);

// التحقق من الاتصال
if ($conn->connect_error) {
    die("فشل الاتصال: " . $conn->connect_error);
}

// تعيين ترميز الأحرف إلى UTF-8
$conn->set_charset("utf8mb4");
?>