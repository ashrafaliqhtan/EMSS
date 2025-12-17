<?php
session_start();
require_once 'db_config.php';

// معالجة بيانات التسجيل عند إرسال النموذج
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // جمع البيانات من النموذج
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    $confirm_password = $_POST['confirm_password'] ?? '';
    $firstname = $_POST['firstname'] ?? '';
    $lastname = $_POST['lastname'] ?? '';
    $email = $_POST['email'] ?? '';
    $phone = $_POST['phone'] ?? '';
    $gender = $_POST['gender'] ?? '';
    $birthdate = $_POST['birthdate'] ?? '';
    $license_number = $_POST['license_number'] ?? '';
    $vehicle_type = $_POST['vehicle_type'] ?? '';
    $vehicle_model = $_POST['vehicle_model'] ?? '';
    $vehicle_color = $_POST['vehicle_color'] ?? '';
    $vehicle_year = $_POST['vehicle_year'] ?? '';
    $vehicle_number = $_POST['vehicle_number'] ?? '';

    // مصفوفة لأخطاء التحقق
    $errors = [];

    // التحقق من البيانات
    if (empty($username)) {
        $errors['username'] = 'اسم المستخدم مطلوب';
    } elseif (strlen($username) < 4) {
        $errors['username'] = 'اسم المستخدم يجب أن يكون 4 أحرف على الأقل';
    }

    if (empty($password)) {
        $errors['password'] = 'كلمة المرور مطلوبة';
    } elseif (strlen($password) < 6) {
        $errors['password'] = 'كلمة المرور يجب أن تكون 6 أحرف على الأقل';
    }

    if ($password !== $confirm_password) {
        $errors['confirm_password'] = 'كلمة المرور غير متطابقة';
    }

    if (empty($firstname)) {
        $errors['firstname'] = 'الاسم الأول مطلوب';
    }

    if (empty($lastname)) {
        $errors['lastname'] = 'الاسم الأخير مطلوب';
    }

    if (empty($email)) {
        $errors['email'] = 'البريد الإلكتروني مطلوب';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'البريد الإلكتروني غير صالح';
    }

    if (empty($phone)) {
        $errors['phone'] = 'رقم الهاتف مطلوب';
    }

    if (empty($gender)) {
        $errors['gender'] = 'الجنس مطلوب';
    }

    if (empty($birthdate)) {
        $errors['birthdate'] = 'تاريخ الميلاد مطلوب';
    }

    if (empty($license_number)) {
        $errors['license_number'] = 'رقم الرخصة مطلوب';
    }

    if (empty($vehicle_type)) {
        $errors['vehicle_type'] = 'نوع المركبة مطلوب';
    }

    if (empty($vehicle_number)) {
        $errors['vehicle_number'] = 'رقم المركبة مطلوب';
    }

    // التحقق من عدم وجود أخطاء
    if (empty($errors)) {
        // التحقق من أن اسم المستخدم غير مستخدم
        $stmt = $conn->prepare("SELECT Driver_id FROM driver WHERE username = ?");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            $errors['username'] = 'اسم المستخدم موجود مسبقاً';
        } else {
            // بدء عملية التسجيل
           // بدء عملية التسجيل
$conn->begin_transaction();

try {
    // 1. تسجيل السائق في جدول driver
    $stmt = $conn->prepare("INSERT INTO driver 
        (username, password, FirstName, lastName, Email, phone, Gender, birthdate, license_number, AccountStatus) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')");
    
    // في تطبيق حقيقي، استخدم password_hash() بدلاً من تخزين كلمة المرور كنص صريح
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);
    $stmt->bind_param("sssssisss", 
        $username, 
        $hashed_password,
        $firstname, 
        $lastname, 
        $email, 
        $phone, 
        $gender, 
        $birthdate, 
        $license_number
    );
    
    if (!$stmt->execute()) {
        throw new Exception("خطأ في تسجيل السائق: " . $stmt->error);
    }
    
    $driver_id = $conn->insert_id;
    
    if (!$driver_id) {
        throw new Exception("لم يتم الحصول على معرف السائق");
    }

    // 2. تسجيل المركبة في جدول vehicles
    $stmt = $conn->prepare("INSERT INTO vehicles 
        (Vehicle_number, Vehicle_Model, Vehicle_Type, license_number, Vehicle_status, Driver_id) 
        VALUES (?, ?, ?, ?, 'active', ?)");
    
    $stmt->bind_param("ssssi", 
        $vehicle_number,
        $vehicle_model,
        $vehicle_type,
        $license_number,
        $driver_id  // ← هنا نمرر قيمة Driver_id
    );
    
    if (!$stmt->execute()) {
        throw new Exception("خطأ في تسجيل المركبة: " . $stmt->error);
    }

    // تأكيد العملية
    $conn->commit();

    // تسجيل الدخول تلقائياً
    $_SESSION['driver_id'] = $driver_id;
    $_SESSION['driver_name'] = $firstname . ' ' . $lastname;

    // توجيه إلى صفحة طلبات الرحلات
    header("Location: driver_requests.php");
    exit();
    
} catch (Exception $e) {
    // التراجع عن العملية في حالة خطأ
    $conn->rollback();
    $errors['general'] = 'حدث خطأ أثناء التسجيل: ' . $e->getMessage();
}
        }
    }
}
?>

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل سائق جديد - معاون</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            font-family: 'Tajawal', sans-serif;
        }
        body {
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #4775f5;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: bold;
        }
        input, select, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .error {
            color: #f44336;
            font-size: 14px;
            margin-top: 5px;
        }
        .form-row {
            display: flex;
            gap: 15px;
        }
        .form-row .form-group {
            flex: 1;
        }
        button {
            background-color: #4775f5;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: background-color 0.3s;
            margin-top: 10px;
        }
        button:hover {
            background-color: #3a62d4;
        }
        .login-link {
            text-align: center;
            margin-top: 20px;
        }
        .login-link a {
            color: #4775f5;
            text-decoration: none;
        }
        .login-link a:hover {
            text-decoration: underline;
        }
        .section-title {
            background-color: #f0f0f0;
            padding: 10px 15px;
            border-radius: 5px;
            margin: 25px 0 15px;
            color: #333;
            font-weight: bold;
        }
        .radio-group {
            display: flex;
            gap: 15px;
            margin-top: 5px;
        }
        .radio-option {
            display: flex;
            align-items: center;
        }
        .radio-option input {
            width: auto;
            margin-left: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>تسجيل سائق جديد</h1>
        
        <?php if (!empty($errors['general'])): ?>
            <div class="error" style="margin-bottom: 20px; text-align: center;"><?php echo $errors['general']; ?></div>
        <?php endif; ?>
        
        <form method="POST" action="">
            <div class="section-title">معلومات الحساب</div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="username">اسم المستخدم *</label>
                    <input type="text" id="username" name="username" value="<?php echo htmlspecialchars($username ?? ''); ?>" required>
                    <?php if (!empty($errors['username'])): ?>
                        <div class="error"><?php echo $errors['username']; ?></div>
                    <?php endif; ?>
                </div>
                
                <div class="form-group">
                    <label for="email">البريد الإلكتروني *</label>
                    <input type="email" id="email" name="email" value="<?php echo htmlspecialchars($email ?? ''); ?>" required>
                    <?php if (!empty($errors['email'])): ?>
                        <div class="error"><?php echo $errors['email']; ?></div>
                    <?php endif; ?>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="password">كلمة المرور *</label>
                    <input type="password" id="password" name="password" required>
                    <?php if (!empty($errors['password'])): ?>
                        <div class="error"><?php echo $errors['password']; ?></div>
                    <?php endif; ?>
                </div>
                
                <div class="form-group">
                    <label for="confirm_password">تأكيد كلمة المرور *</label>
                    <input type="password" id="confirm_password" name="confirm_password" required>
                    <?php if (!empty($errors['confirm_password'])): ?>
                        <div class="error"><?php echo $errors['confirm_password']; ?></div>
                    <?php endif; ?>
                </div>
            </div>
            
            <div class="section-title">المعلومات الشخصية</div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="firstname">الاسم الأول *</label>
                    <input type="text" id="firstname" name="firstname" value="<?php echo htmlspecialchars($firstname ?? ''); ?>" required>
                    <?php if (!empty($errors['firstname'])): ?>
                        <div class="error"><?php echo $errors['firstname']; ?></div>
                    <?php endif; ?>
                </div>
                
                <div class="form-group">
                    <label for="lastname">الاسم الأخير *</label>
                    <input type="text" id="lastname" name="lastname" value="<?php echo htmlspecialchars($lastname ?? ''); ?>" required>
                    <?php if (!empty($errors['lastname'])): ?>
                        <div class="error"><?php echo $errors['lastname']; ?></div>
                    <?php endif; ?>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="phone">رقم الهاتف *</label>
                    <input type="tel" id="phone" name="phone" value="<?php echo htmlspecialchars($phone ?? ''); ?>" required>
                    <?php if (!empty($errors['phone'])): ?>
                        <div class="error"><?php echo $errors['phone']; ?></div>
                    <?php endif; ?>
                </div>
                
                <div class="form-group">
                    <label for="license_number">رقم الرخصة *</label>
                    <input type="text" id="license_number" name="license_number" value="<?php echo htmlspecialchars($license_number ?? ''); ?>" required>
                    <?php if (!empty($errors['license_number'])): ?>
                        <div class="error"><?php echo $errors['license_number']; ?></div>
                    <?php endif; ?>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>الجنس *</label>
                    <div class="radio-group">
                        <div class="radio-option">
                            <input type="radio" id="male" name="gender" value="ذكر" <?php echo ($gender ?? '') === 'ذكر' ? 'checked' : ''; ?> required>
                            <label for="male">ذكر</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" id="female" name="gender" value="أنثى" <?php echo ($gender ?? '') === 'أنثى' ? 'checked' : ''; ?>>
                            <label for="female">أنثى</label>
                        </div>
                    </div>
                    <?php if (!empty($errors['gender'])): ?>
                        <div class="error"><?php echo $errors['gender']; ?></div>
                    <?php endif; ?>
                </div>
                
                <div class="form-group">
                    <label for="birthdate">تاريخ الميلاد *</label>
                    <input type="date" id="birthdate" name="birthdate" value="<?php echo htmlspecialchars($birthdate ?? ''); ?>" required>
                    <?php if (!empty($errors['birthdate'])): ?>
                        <div class="error"><?php echo $errors['birthdate']; ?></div>
                    <?php endif; ?>
                </div>
            </div>
            
            <div class="section-title">معلومات المركبة</div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="vehicle_type">نوع المركبة *</label>
                    <select id="vehicle_type" name="vehicle_type" required>
                        <option value="">اختر نوع المركبة</option>
                        <option value="سيارة" <?php echo ($vehicle_type ?? '') === 'سيارة' ? 'selected' : ''; ?>>سيارة</option>
                        <option value="فان" <?php echo ($vehicle_type ?? '') === 'فان' ? 'selected' : ''; ?>>فان</option>
                        <option value="حافلة صغيرة" <?php echo ($vehicle_type ?? '') === 'حافلة صغيرة' ? 'selected' : ''; ?>>حافلة صغيرة</option>
                    </select>
                    <?php if (!empty($errors['vehicle_type'])): ?>
                        <div class="error"><?php echo $errors['vehicle_type']; ?></div>
                    <?php endif; ?>
                </div>
                
                <div class="form-group">
                    <label for="vehicle_model">طراز المركبة</label>
                    <input type="text" id="vehicle_model" name="vehicle_model" value="<?php echo htmlspecialchars($vehicle_model ?? ''); ?>">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="vehicle_color">لون المركبة</label>
                    <input type="text" id="vehicle_color" name="vehicle_color" value="<?php echo htmlspecialchars($vehicle_color ?? ''); ?>">
                </div>
                
                <div class="form-group">
                    <label for="vehicle_year">سنة الصنع</label>
                    <input type="number" id="vehicle_year" name="vehicle_year" min="1900" max="<?php echo date('Y'); ?>" 
                           value="<?php echo htmlspecialchars($vehicle_year ?? ''); ?>">
                </div>
            </div>
            
            <div class="form-group">
                <label for="vehicle_number">رقم المركبة *</label>
                <input type="text" id="vehicle_number" name="vehicle_number" value="<?php echo htmlspecialchars($vehicle_number ?? ''); ?>" required>
                <?php if (!empty($errors['vehicle_number'])): ?>
                    <div class="error"><?php echo $errors['vehicle_number']; ?></div>
                <?php endif; ?>
            </div>
            
            <button type="submit">تسجيل حساب جديد</button>
        </form>
        
        <div class="login-link">
            لديك حساب بالفعل؟ <a href="login.php">سجل دخول هنا</a>
        </div>
    </div>
</body>
</html>