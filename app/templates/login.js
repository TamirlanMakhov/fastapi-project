const loginForm = document.getElementById("login-form");
const responseDiv = document.getElementById("response");

const loginUser = async (event) => {
  event.preventDefault();

  const formData = new FormData(loginForm);
  const data = {
    email: formData.get("email"),
    password: formData.get("password"),
  };

  const response = await fetch("/users/login", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  });

  const result = await response.json();

  if (response.status === 200) {
    responseDiv.innerHTML = `<p>Welcome ${result.email}!</p>`;
  } else {
    responseDiv.innerHTML = `<p>${result.detail}</p>`;
  }
};
