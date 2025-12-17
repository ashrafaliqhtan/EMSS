<?php
session_start();
require_once 'db_config.php';

// التحقق من أن السائق مسجل دخول
if (!isset($_SESSION['driver_id'])) {
    header("Location: login.php");
    exit();
}

// استعلام للحصول على طلبات الرحلات المتاحة
$query = "SELECT t.*, c.Firstname, c.lastName, c.disabilty_type 
          FROM trips t
          JOIN customer c ON t.customer_id = c.customer_Id
          WHERE t.Driver_id IS NULL AND t.Trip_Status = 'pending'";

$result = $conn->query($query);
$trips = $result->fetch_all(MYSQLI_ASSOC);
?>

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>طلبات الرحلات - معاون</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Tajawal', sans-serif;
        }
        
        body {
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background-color: #4775f5;
            color: white;
            padding: 15px 0;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .request-card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .customer-info {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .customer-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background-color: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: 15px;
            font-size: 24px;
            color: #555;
        }
        
        .customer-details h3 {
            margin-bottom: 5px;
            color: #4775f5;
        }
        
        .trip-details {
            margin: 15px 0;
        }
        
        .trip-details p {
            margin-bottom: 8px;
        }
        
        .location-map {
            height: 200px;
            background-color: #e9e9e9;
            border-radius: 8px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        
        .map-placeholder {
            text-align: center;
            color: #666;
        }
        
        .action-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        
        .btn {
            padding: 10px 25px;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-accept {
            background-color: #4CAF50;
            color: white;
        }
        
        .btn-reject {
            background-color: #f44336;
            color: white;
        }
        
        .btn:hover {
            opacity: 0.9;
            transform: translateY(-2px);
        }
        
        .no-requests {
            text-align: center;
            padding: 50px;
            color: #666;
        }
        
        /* تنسيقات الخريطة */
        .map-container {
            width: 100%;
            height: 100%;
        }
        
        header {
      text-align: center;
      padding: 20px 0;
    }
    /* شريط التنقل */
    nav {
      background-color: #4775f5;
    }
    nav ul {
      list-style: none;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 10px 0;
    }
    nav ul li {
      margin: 0 30px;
    }
    nav ul li a {
      text-decoration: none;
      color: #000;
      font-size: 18px;
      font-weight: 500;
    }
        
        
    </style>
    
    
</head>
<body>
   <header>
    <img src="logo.jpg"  height="44px"  alt="شعار معاون">
    
            <h1>طلبات الرحلات الواردة</h1>
  
    
  </header>

  <!-- شريط التنقل -->
  <nav>
    <ul>
      <li><a href="#">الصفحة الرئيسية</a></li>
      <li><a href="register.php">إنشاء حساب</a></li>
      <li><a href="login.php">تسجيل دخول</a></li>
      <li><a href="#">تواصل معنا</a></li>
    </ul>
  </nav>
  
  
    <header>
  </header>
    
    <div class="container">
        <?php if (count($trips) > 0): ?>
            <?php foreach ($trips as $trip): ?>
                <div class="request-card" id="trip-<?php echo $trip['Trip_id']; ?>">
                    <div class="customer-info">
                        <div class="customer-avatar"><?php echo mb_substr($trip['Firstname'], 0, 1); ?></div>
                        <div class="customer-details">
                            <h3><?php echo $trip['Firstname'] . ' ' . $trip['lastName']; ?></h3>
                            <p><?php echo $trip['disabilty_type']; ?></p>
                        </div>
                    </div>
                    
                    <div class="trip-details">
                        <p><strong>نقطة الانطلاق:</strong> <?php echo $trip['Meeting_Location']; ?></p>
                        <p><strong>الوجهة:</strong> <?php echo $trip['Destination_Location']; ?></p>
                        <p><strong>نوع المركبة:</strong> <?php echo $trip['Vehicle_Type']; ?></p>
                        <p><strong>تاريخ الرحلة:</strong> <?php echo $trip['Trip_Date']; ?></p>
                        <p><strong>يحتاج مرافق:</strong> <?php echo $trip['companion_Service'] ? 'نعم (' . $trip['companion_Gender'] . ')' : 'لا'; ?></p>
                    </div>
                    
                    <div class="location-map" id="map-<?php echo $trip['Trip_id']; ?>">
                        <div class="map-placeholder">
                            <p>جاري تحميل الخريطة...</p>
                        </div>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="btn btn-reject" onclick="rejectRequest(<?php echo $trip['Trip_id']; ?>)">رفض الطلب</button>
                        <button class="btn btn-accept" onclick="acceptRequest(<?php echo $trip['Trip_id']; ?>)">قبول الطلب</button>
                    </div>
                </div>
            <?php endforeach; ?>
        <?php else: ?>
            <div class="no-requests">
                <p>لا توجد طلبات رحلات متاحة حالياً</p>
            </div>
        <?php endif; ?>
    </div>

    <!-- مكتبة Leaflet للخرائط -->
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    
    <script>
        // دالة لتهيئة الخرائط
        function initMaps() {
            <?php foreach ($trips as $trip): ?>
                // إنشاء خريطة لكل رحلة
                const map<?php echo $trip['Trip_id']; ?> = L.map('map-<?php echo $trip['Trip_id']; ?>').setView([24.7136, 46.6753], 15);
                
                // إضافة طبقة الخريطة من OpenStreetMap
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(map<?php echo $trip['Trip_id']; ?>);
                
                // إضافة علامة للموقع (هنا نستخدم إحداثيات افتراضية)
                L.marker([24.7136, 46.6753]).addTo(map<?php echo $trip['Trip_id']; ?>)
                    .bindPopup("موقع العميل")
                    .openPopup();
            <?php endforeach; ?>
        }
        
        // تهيئة الخرائط عند تحميل الصفحة
        window.onload = initMaps;
        
        // دالة لقبول الطلب
        function acceptRequest(tripId) {
            fetch('process_request.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `action=accept&trip_id=${tripId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('تم قبول الطلب بنجاح');
                    document.getElementById(`trip-${tripId}`).remove();
                } else {
                    alert('حدث خطأ: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('حدث خطأ أثناء معالجة الطلب');
            });
        }
        
        // دالة لرفض الطلب
        function rejectRequest(tripId) {
            fetch('process_request.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `action=reject&trip_id=${tripId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('تم رفض الطلب بنجاح');
                    document.getElementById(`trip-${tripId}`).remove();
                } else {
                    alert('حدث خطأ: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('حدث خطأ أثناء معالجة الطلب');
            });
        }
    </script>
</body>
</html>