function checkAuth() {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "/";
  }
}

let token = localStorage.getItem("token");

function login() {
  fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    }),
  })
    .then((r) => r.json())
    .then((data) => {
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "/dashboard";
      } else {
        document.getElementById("result").innerText = data.message;
      }
    });
}

function register() {
  fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: document.getElementById("username").value,
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    }),
  })
    .then((r) => r.json())
    .then((data) => {
      if (data.message === "User registered successfully") {
        const result = document.getElementById("result");
        result.style.color = "green";
        result.innerText = "Регистрация прошла успешно. Выполняется вход...";

        setTimeout(() => {
          fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: document.getElementById("email").value,
              password: document.getElementById("password").value,
            }),
          })
            .then((r) => r.json())
            .then((loginData) => {
              localStorage.setItem("token", loginData.access_token);
              window.location.href = "/dashboard";
            });
        }, 1000);
      } else {
        document.getElementById("result").innerText = data.message;
      }
    });
}
