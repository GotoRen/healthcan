/*------------------------------------
### Created by K18039-後藤 廉 
--------------------------------------
### 内容：データの計算 
### ファイル：healthcan_form.js
--------------------------------------*/

function resolve_calculation() {
    let height = document.getElementById("form-height").value;
    let weight = document.getElementById("form-weight").value;
    let h = parseFloat(height)/100;
    let w = parseFloat(weight);
    let bmi = w/(Math.pow(h, 2));       // BMI: kg/(m)^2
    let pro_weight = Math.pow(h, 2)*22; // 適正体重: (cm)^2*22
    let diff_weight = w-pro_weight;     // 適正体重との差: 体重-適正体重  
    document.getElementById("form-bmi").value = bmi.toFixed(1);
    document.getElementById("form-pro_weight").value = pro_weight.toFixed(2);
    document.getElementById("form-diff_weight").value = diff_weight.toFixed(2);
}
