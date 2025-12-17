<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>معاون</title>
  <!-- استدعاء خط تجوّال العربي -->
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: 'Tajawal', sans-serif;
      background-color: #f0f1f5;
      color: #000;
      line-height: 1.5;
      background: #f0f1f5;
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
    /* القسم الرئيسي */
    .hero {
      background-color: #f2f2f2;
      text-align: center;
      padding: 50px 20px 0;
      position: relative;
    }
    .hero img {
      width: 120px;
      height: auto;
    }
    .hero h1 {
      margin: 15px 0 5px;
      font-size: 36px;
      font-weight: 700;
    }
    .hero h2 {
      margin-bottom: 15px;
      font-size: 24px;
      font-weight: 500;
    }
    .hero p {
      font-size: 18px;
      margin-bottom: 10px;
    }
    /* موجات أسفل الصفحة - ثابتة */
    .waves {
      position: relative;
      height: 150px;
      margin-top: 20px;
    }
    .wave {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 100px;
    }
    .wave-1 {
      background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1200 120" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"><path d="M0,0 C150,80 450,20 750,70 C1050,120 1200,60 1200,60 L1200,120 L0,120 Z" fill="%234775f5"/></svg>');
      background-size: cover;
      background-repeat: no-repeat;
      z-index: 3;
      opacity: 0.8;
    }
    .wave-2 {
      background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1200 120" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"><path d="M0,0 C200,50 400,100 600,50 C800,0 1000,100 1200,50 L1200,120 L0,120 Z" fill="%2342A5F5"/></svg>');
      background-size: cover;
      background-repeat: no-repeat;
      z-index: 2;
      opacity: 0.6;
    }
    .wave-3 {
      background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1200 120" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"><path d="M0,0 C150,30 450,60 750,30 C1050,0 1200,30 1200,30 L1200,120 L0,120 Z" fill="%23007bff"/></svg>');
      background-size: cover;
      background-repeat: no-repeat;
      z-index: 1;
      opacity: 0.4;
    }
  </style>
</head>
<body>

  <!-- الشعار أعلى الصفحة -->
  <header>
    <img src="logo.jpg"  height="44px"  alt="شعار معاون">
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

  <!-- القسم التعريفي -->
  <section class="hero">
    <img src="logo.jpg"  height="44px"  alt="شعار معاون">
    <h1>معاون</h1>
    <h2>من نحن؟</h2>
    <p>تطبيق توصيل متخصص لذوي الهمم</p>
    <p>يهدف إلى تحسين سبل الراحة لهم وتسهيل عملية تنقلهم</p>

    <!-- موجات ثابتة -->
    <div class="waves">
      <div class="wave wave-1"></div>
      <div class="wave wave-2"></div>
      <div class="wave wave-3"></div>
    </div>
  </section>

</body>
</html>