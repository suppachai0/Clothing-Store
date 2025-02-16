document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("checkout-form");
    const paymentMethodSelect = document.getElementById("payment_method");
    const creditCardSection = document.getElementById("credit-card-section");
    const paypalSection = document.getElementById("paypal-section");
    const errorMessagesDiv = document.getElementById("error-messages");

    // ฟังก์ชันแสดง/ซ่อนฟิลด์ตามวิธีการชำระเงิน
    paymentMethodSelect.addEventListener("change", function () {
        creditCardSection.classList.add("hidden");
        paypalSection.classList.add("hidden");

        if (this.value === "credit_card") {
            creditCardSection.classList.remove("hidden");
        } else if (this.value === "paypal") {
            paypalSection.classList.remove("hidden");
        }
    });

    // ฟังก์ชันตรวจสอบข้อมูลก่อนส่งฟอร์ม
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        errorMessagesDiv.innerHTML = ""; // ล้างข้อความเก่า

        const fullname = document.getElementById("fullname").value.trim();
        const phoneNumber = document.getElementById("phone_number").value.trim();
        const postalCode = document.getElementById("postal_code").value.trim();
        const paymentMethod = paymentMethodSelect.value;
        const creditCardNumber = document.getElementById("credit_card_number").value.trim();
        const paypalEmail = document.getElementById("paypal_email").value.trim();

        let errors = [];

        if (fullname.length < 3) {
            errors.push("⚠️ กรุณากรอกชื่อ-นามสกุลให้ถูกต้อง");
        }

        if (!/^\d{10}$/.test(phoneNumber)) {
            errors.push("⚠️ เบอร์โทรศัพท์ต้องมี 10 หลักและเป็นตัวเลขเท่านั้น");
        }

        if (!/^\d{5}$/.test(postalCode)) {
            errors.push("⚠️ รหัสไปรษณีย์ต้องมี 5 หลักและเป็นตัวเลขเท่านั้น");
        }

        if (paymentMethod === "credit_card" && !/^\d{16}$/.test(creditCardNumber)) {
            errors.push("⚠️ หมายเลขบัตรเครดิตต้องเป็นตัวเลข 16 หลัก");
        }

        if (paymentMethod === "paypal" && !validateEmail(paypalEmail)) {
            errors.push("⚠️ กรุณากรอกอีเมล PayPal ให้ถูกต้อง");
        }

        if (errors.length > 0) {
            displayErrors(errors);
        } else {
            form.submit();
        }
    });

    // ฟังก์ชันตรวจสอบอีเมล
    function validateEmail(email) {
        return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
    }

    // ฟังก์ชันแสดงข้อความผิดพลาด
    function displayErrors(errors) {
        errors.forEach(error => {
            const p = document.createElement("p");
            p.textContent = error;
            p.classList.add("error-text");
            errorMessagesDiv.appendChild(p);
        });
    }
});
