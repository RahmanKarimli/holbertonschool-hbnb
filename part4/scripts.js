document.addEventListener('DOMContentLoaded', () => {
  let allPlaces = [];

  const loginForm = document.getElementById('login-form');

  const isPlacePage = document.location.href.includes("place.html");
  const isIndexPage = document.location.href.includes("index.html");

  if (isIndexPage) {
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

  if (isPlacePage || isIndexPage) {
    checkAuthentication();
  }

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      await loginUser(email, password);
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

  //

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop().split(';').shift();
    }
    return null;
  }


  function checkAuthentication() {
    const loginLink = document.getElementById("login-link");
    const addReviewSection = document.getElementById('add-review');
    const token = getCookie('tokenJWT');

    if (!loginLink) {
      console.error('Login link not found!');
      return;
    }
    if (isPlacePage) {
      if (!addReviewSection) {
        console.error('Add review section not found!');
        return;
      }
    }

    if (!token) {
      loginLink.style.display = 'block';
      if (isPlacePage) {
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
            if (isPlacePage) {
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
    if (isPlacePage) {
      const placeId = getPlaceIdFromURL();
      fetchPlaceDetails(placeId);
    }
  }


  async function fetchPlaces() {
    fetch("http://127.0.0.1:8000/api/v1/places", {
      method: "GET",
    })
      .then(async response => {
        if (response.ok) {
          const placeResponse = await response.json();
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
    const places_list = document.getElementById("places-list");
    places_list.innerHTML = '';

    places.forEach(place => {
      const placeDiv = document.createElement('div');

      let url = new URL("http://localhost:63342/AirBnb/part4/place.html");
      url.searchParams.append('place_id', place.id);

      placeDiv.className = "place-card";
      placeDiv.innerHTML = `
            <h3>${place.title}</h3>
            <p>Price: $${place.price} per night</p>
            <button class="details-button" onclick="window.location.href='${url.href}'">View Details</button>
        `
      places_list.appendChild(placeDiv);
    })
  }

  function getPlaceIdFromURL() {
    const search = window.location.search;
    const params = new URLSearchParams(search);

    return params.get("place_id");
  }

  async function fetchPlaceDetails(placeId) {
    fetch(`http://127.0.0.1:8000/api/v1/places/${placeId}`, {
      method: "GET",
    })
      .then(async response => {
        if (response.ok) {
          const placeResponseById = await response.json();
          displayPlaceDetails(placeResponseById);
        } else {
          throw new Error('Failed to fetch place');
        }
      })
      .catch(error => {
        console.error(error);
        alert('Error fetching place.');
      });
  }

  function displayPlaceDetails(place) {
    const placeDetails = document.getElementById("place-details");
    placeDetails.innerHTML = '';

    const placeDiv = document.createElement('div');

    placeDiv.className = "card place-card";
    placeDiv.innerHTML = `
            <h2>${place.title}</h2>
            <p>Description: ${place.description}</p>
            <p>Location: ${place.latitude}  ${place.longitude}</p>
            `
    placeDetails.append(placeDiv);
  }
});
