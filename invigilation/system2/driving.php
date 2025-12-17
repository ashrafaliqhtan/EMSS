<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>طلبات العملاء – حساب السائق</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    


    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Tajawal', sans-serif;
      background-color: #f2f2f2;
      color: #000;
      line-height: 1.5;
    }
    header { text-align: center; padding: 20px 0; }
    nav {
      
      
      background-color: #4775f5;
      margin-bottom: 20px;
    }
    nav ul {
      list-style: none;
      display: flex;
      justify-content: center;
      padding: 10px 0;
    }
    nav ul li { margin: 0 20px; }
    nav ul li a {
      text-decoration: none;
      color: #000;
      font-size: 18px;
      font-weight: 500;
    }
    main { max-width: 900px; margin: auto; padding: 0 15px; }
    h2 { margin-bottom: 15px; font-size: 28px; }
    .request {
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      padding: 15px;
      margin-bottom: 20px;
    }
    .request h3 { font-size: 22px; margin-bottom: 5px; }
    .request p { margin-bottom: 10px; }
    .map {
      width: 100%;
      height: 250px;
      border-radius: 6px;
      margin-bottom: 10px;
    }
    .actions {
      text-align: center;
    }
    .actions button {
      padding: 8px 20px;
      margin: 0 10px;
      font-size: 16px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    .actions .accept { background-color: #4CAF50; color: #fff; }
    .actions .reject { background-color: #F44336; color: #fff; }
 


  </style>
</head>
<body>
 <!-- شعار ومعنون -->
  <header>
    <img src="logo.jpg"  height="44px"  alt="شعار معاون">
    <h1>حساب السائق</h1>
  </header>

  <!-- شريط التنقل -->
  <nav>
    <ul>
      <li><a href="#">الرئيسية</a></li>
      <li><a href="#">طلبات العملاء</a></li>
      <li><a href="#">تواصل معنا</a></li>
      <li><a href="#">تسجيل خروج</a></li>
    </ul>
  </nav>
<h2>طلبات العملاء</h2>
<div id="requests"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
fetch('get_requests.php')
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById('requests');
    data.forEach((req, index) => {
      const div = document.createElement('div');
      div.className = 'request';
      div.innerHTML = `
        <h3>العميل: ${req.customer_name}</h3>
        <p>المدينة: ${req.city}</p>
        <div class="map" id="map${index}"></div>
        <button class="accept">قبول</button>
        <button class="reject">رفض</button>
      `;
      container.appendChild(div);

      // عرض الخريطة
      const map = L.map('map' + index).setView([req.latitude, req.longitude], 13);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);
      L.marker([req.latitude, req.longitude]).addTo(map);
    });
  });
</script>

</body>
</html>