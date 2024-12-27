

DELETE THIS FILE

DELETE THIS THIS FILE

THIS IS USELESS


function checkAuthenticationPlace() {
  const loginLink = document.getElementById("login-link");
  const addReviewSection = document.getElementById('add-review');
  const token = getCookie('tokenJWT');

  if (!loginLink) {
    console.error('Login link not found!');
    return;
  }
  if (!addReviewSection) {
    console.error('Add review section not found!');
    return;
  }

  if (!token) {
    loginLink.style.display = 'block';
    addReviewSection.style.display = 'none';
  } else {
    if (token) {
      loginLink.style.display = 'none';
      addReviewSection.style.display = 'block';
    } else {
      document.cookie = 'tokenJWT=';
      window.location.href = 'http://localhost:63342/AirBnb/part4/login.html';
    }
  }
  const placeId = getPlaceIdFromURL();
  fetchPlaceDetails(placeId);
}



function checkAuthenticationIndex() {
  const loginLink = document.getElementById("login-link");
  const token = getCookie('tokenJWT');

  if (!loginLink) {
    console.error('Login link not found!');
    return;
  }

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    fetch("http://127.0.0.1:8000/api/v1/auth/verify", {
      method: "POST", headers: {
        "Authorization": `Bearer ${token}`,
      }
    })
      .then(response => {
        if (response.ok) {
          loginLink.style.display = 'none';
        } else {
          document.cookie = 'tokenJWT=';
          window.location.href = 'http://localhost:63342/AirBnb/part4/login.html';
        }
      })
      .catch(() => {
        document.cookie = 'tokenJWT=';
        window.location.href = 'http://localhost:63342/AirBnb/part4/login.html';
      });
  }
}



function checkAuthentication() {
  const loginLink = document.getElementById("login-link");
  const token = getCookie('tokenJWT');

  if (!loginLink) {
    console.error('Login link not found!');
    return;
  }
  if (document.location.pathname.includes("place.html")) {
    const addReviewSection = document.getElementById('add-review');
    if (!addReviewSection) {
      console.error('Add review section not found!');
      return;
    }
  }

  if (!token) {
    loginLink.style.display = 'block';
    if (document.location.pathname.includes("place.html")) {
      addReviewSection.style.display = 'none';
    }
  } else {
    fetch("http://127.0.0.1:8000/api/v1/auth/verify", {
      method: "POST", headers: {
        "Authorization": `Bearer ${token}`,
      }
    })
    .then(response => {
        if (response.ok) {
          loginLink.style.display = 'none';
          if (document.location.pathname.includes("place.html")) {
            addReviewSection.style.display = 'block';
          }
        } else {
          document.cookie = 'tokenJWT=';
          window.location.href = 'http://localhost:63342/AirBnb/part4/login.html';
        }
      })
      .catch(() => {
        document.cookie = 'tokenJWT=';
        window.location.href = 'http://localhost:63342/AirBnb/part4/login.html';
      });
  }
  if (document.location.pathname.includes("place.html")) {
    const placeId = getPlaceIdFromURL();
    fetchPlaceDetails(placeId);
  }
}












