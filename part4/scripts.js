document.addEventListener('DOMContentLoaded', () => {
  let allPlaces = [];

  const loginForm = document.getElementById('login-form');

  if (document.location.href.includes("index.html")) {
    fetchPlaces();

    document.getElementById('price-filter').addEventListener('change', (event) => {
      const selectedPrice = event.target.value;

      if (selectedPrice === "All") {
        displayPlaces(allPlaces);
      } else {
        const maxPrice = parseFloat(selectedPrice);
        displayPlaces(allPlaces.filter((place) => place.price <= maxPrice));
      }
    });
  }

  checkAuthentication();

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById("email").value
      const password = document.getElementById("password").value

      await loginUser(email, password)
    });
  }

  async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:8000/api/v1/auth/login', {
      method: 'POST', headers: {
        'Content-Type': 'application/json'
      }, body: JSON.stringify({email: email, password: password})
    });
    if (response.ok) {
      const data = await response.json();
      document.cookie = `tokenJWT=${data.access_token}; path=/AirBnb/part4`;

      window.location.href = 'http://localhost:63342/AirBnb/part4/index.html';
    } else {
      alert('Login failed: ' + response.statusText);
    }
  }

  function checkAuthentication() {
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

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop().split(';').shift();
    }
    return null;
  }


  async function fetchPlaces() {
    fetch("http://127.0.0.1:8000/api/v1/places", {
      method: "GET",
    })
      .then(async response => {
        if (response.ok) {
          placeResponse = await response.json();
          allPlaces = placeResponse;
          displayPlaces(placeResponse);
        } else {
          throw new Error('Failed to fetch places');
        }
      })
      .catch(error => {
        console.error(error);
        alert('Error fetching places.');
      });
  }

  function displayPlaces(places) {
    let places_list = document.getElementById("places-list");
    places_list.innerHTML = '';

    places.forEach(place => {
      placeDiv = document.createElement('div');

      placeDiv.className = "place-card"
      placeDiv.innerHTML = `
            <h3>${place.title}</h3>
            <p>Price: $${place.price} per night</p>
            <button class="details-button" onclick="window.location.href='place.html';">View Details</button>
        `

      places_list.appendChild(placeDiv);
    })
  }
});
