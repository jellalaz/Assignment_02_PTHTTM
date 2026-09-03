/**
 * Assignment 02 — Frontend Controller
 * Uses relative API paths (/predict/...) for 100% LAN & multi-device compatibility.
 */

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initDiabetesForm();
  initHouseForm();
  initEcommerceForm();
});

// Tab Navigation
function initTabs() {
  const buttons = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('.tab-panel');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');

      buttons.forEach(b => b.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const activePanel = document.getElementById(targetTab);
      if (activePanel) {
        activePanel.classList.add('active');
      }
    });
  });
}

// ---------------------------------------------------------------------------
// 1. Diabetes Prediction Controller
// ---------------------------------------------------------------------------
function initDiabetesForm() {
  const form = document.getElementById('form-diabetes');
  const placeholder = document.getElementById('diabetes-placeholder');
  const resultContainer = document.getElementById('diabetes-result');
  const btn = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    btn.disabled = true;
    btn.innerHTML = '<span>Đang xử lý...</span>';

    const payload = {
      gender: document.getElementById('dia-gender').value,
      age: parseFloat(document.getElementById('dia-age').value),
      hypertension: parseInt(document.getElementById('dia-hypertension').value),
      heart_disease: parseInt(document.getElementById('dia-heart-disease').value),
      smoking_history: document.getElementById('dia-smoking').value,
      bmi: parseFloat(document.getElementById('dia-bmi').value),
      HbA1c_level: parseFloat(document.getElementById('dia-hba1c').value),
      blood_glucose_level: parseInt(document.getElementById('dia-glucose').value)
    };

    try {
      // Relative URL guarantees LAN mobile compatibility
      const res = await fetch('/predict/diabetes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Dự đoán thất bại');
      }

      const data = await res.json();
      displayDiabetesResult(data);
    } catch (err) {
      alert('Lỗi dự đoán tiểu đường: ' + err.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<span>⚡ Dự đoán</span>';
    }
  });

  function displayDiabetesResult(data) {
    placeholder.style.display = 'none';
    resultContainer.classList.add('show');

    const badge = document.getElementById('dia-badge');
    const metricHuge = document.getElementById('dia-prob-huge');
    const gaugeFill = document.getElementById('dia-gauge-fill');
    const probLabel = document.getElementById('dia-prob-label');
    const riskLabel = document.getElementById('dia-risk-level');

    const pct = (data.probability * 100).toFixed(1);

    if (data.prediction === 1) {
      badge.className = 'status-badge badge-danger';
      badge.innerText = '⚠️ ' + data.diagnosis;
      metricHuge.className = 'metric-value-huge negative';
      gaugeFill.style.backgroundColor = '#ef4444';
    } else {
      badge.className = 'status-badge badge-success';
      badge.innerText = '✅ ' + data.diagnosis;
      metricHuge.className = 'metric-value-huge positive';
      gaugeFill.style.backgroundColor = '#10b981';
    }

    metricHuge.innerText = pct + '%';
    gaugeFill.style.width = pct + '%';
    probLabel.innerText = data.probability.toFixed(4);
    riskLabel.innerText = data.risk_level;
  }
}

// ---------------------------------------------------------------------------
// 2. House Price Prediction Controller
// ---------------------------------------------------------------------------
function initHouseForm() {
  const form = document.getElementById('form-house');
  const placeholder = document.getElementById('house-placeholder');
  const resultContainer = document.getElementById('house-result');
  const btn = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    btn.disabled = true;
    btn.innerHTML = '<span>Đang định giá...</span>';

    const payload = {
      Area: parseFloat(document.getElementById('house-area').value),
      Bedrooms: parseInt(document.getElementById('house-bedrooms').value),
      Bathrooms: parseInt(document.getElementById('house-bathrooms').value),
      Stories: parseInt(document.getElementById('house-stories').value),
      Parking: parseInt(document.getElementById('house-parking').value),
      Age: parseInt(document.getElementById('house-age').value),
      City: document.getElementById('house-city').value,
      Furnishing: document.getElementById('house-furnishing').value,
      "Main Road": document.getElementById('house-mainroad').value,
      "Guest Room": document.getElementById('house-guestroom').value,
      Basement: document.getElementById('house-basement').value,
      "Water Supply": document.getElementById('house-watersupply').value,
      "Air Conditioning": document.getElementById('house-ac').value,
      "Preferred Tenant": document.getElementById('house-tenant').value,
      "Locality Rating": parseInt(document.getElementById('house-locality').value)
    };

    try {
      const res = await fetch('/predict/house', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Định giá thất bại');
      }

      const data = await res.json();
      displayHouseResult(data);
    } catch (err) {
      alert('Lỗi định giá nhà: ' + err.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<span>⚡ Định giá Bất động sản</span>';
    }
  });

  function displayHouseResult(data) {
    placeholder.style.display = 'none';
    resultContainer.classList.add('show');

    document.getElementById('house-price-huge').innerText = data.formatted_price;
    document.getElementById('house-raw-price').innerText = '$' + data.predicted_price.toLocaleString();
  }
}

// ---------------------------------------------------------------------------
// 3. E-Commerce Customer Behavior Controller
// ---------------------------------------------------------------------------
function initEcommerceForm() {
  const form = document.getElementById('form-ecommerce');
  const placeholder = document.getElementById('ecom-placeholder');
  const resultContainer = document.getElementById('ecom-result');
  const btn = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    btn.disabled = true;
    btn.innerHTML = '<span>Đang phân tích...</span>';

    const payload = {
      Age: parseInt(document.getElementById('ecom-age').value),
      Rating: parseInt(document.getElementById('ecom-rating').value),
      "Positive Feedback Count": parseInt(document.getElementById('ecom-feedback').value),
      "Division Name": document.getElementById('ecom-division').value,
      "Department Name": document.getElementById('ecom-dept').value,
      "Class Name": document.getElementById('ecom-class').value,
      "Review Text": document.getElementById('ecom-review').value
    };

    try {
      const res = await fetch('/predict/ecommerce', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Dự đoán E-commerce thất bại');
      }

      const data = await res.json();
      displayEcommerceResult(data);
    } catch (err) {
      alert('Lỗi phân tích hành vi: ' + err.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<span>⚡ Phân tích / Dự đoán</span>';
    }
  });

  function displayEcommerceResult(data) {
    placeholder.style.display = 'none';
    resultContainer.classList.add('show');

    const badge = document.getElementById('ecom-badge');
    const metricHuge = document.getElementById('ecom-conf-huge');
    const gaugeFill = document.getElementById('ecom-gauge-fill');
    const sentimentLabel = document.getElementById('ecom-sentiment');

    const pct = (data.confidence * 100).toFixed(1);

    if (data.recommended === 1) {
      badge.className = 'status-badge badge-success';
      badge.innerText = '⭐ ' + data.recommendation_label;
      metricHuge.className = 'metric-value-huge positive';
      gaugeFill.style.backgroundColor = '#10b981';
    } else {
      badge.className = 'status-badge badge-danger';
      badge.innerText = '❌ ' + data.recommendation_label;
      metricHuge.className = 'metric-value-huge negative';
      gaugeFill.style.backgroundColor = '#ef4444';
    }

    metricHuge.innerText = pct + '%';
    gaugeFill.style.width = pct + '%';
    sentimentLabel.innerText = data.sentiment_hint;
  }
}
