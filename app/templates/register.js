const registrationHeader = document.getElementById("registration-header");
const registrationForm = document.getElementById("registration-form");
const responseDiv = document.getElementById("response");

const registerUser = async (event) => {
  event.preventDefault();

  const formData = new FormData(registrationForm);
  const data = {
    email: formData.get("email"),
    password: formData.get("password"),
  };

  const response = await fetch("/users/signup", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  });

  const result = await response.json();

  registrationHeader.innerHTML = "Вы успешно создали пользователя";
  registrationForm.style.display = "none";

  responseDiv.innerHTML = `
    <div class="bg-green-200 rounded p-4">
      <p>User ID: ${result.id}</p>
      <p>Email: ${result.email}</p>
    </div>
    <div class="flex justify-center mt-4">
      <button class="bg-gray-600 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-full mr-4" onclick="goToLoginPage()">Login</button>
      <button class="bg-gray-600 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-full" onclick="goToHomePage()">Main page</button>
    </div>
  `;
};

const goToLoginPage = () => {
  window.location.href = "/users/login";
};

const goToHomePage = () => {
  window.location.href = "/";
};
