document.addEventListener('DOMContentLoaded', function() {
    initGeolocation();

    const searchInput = document.getElementById('restaurant-search');
    const restaurantList = document.getElementById('restaurant-list');
    if (searchInput && restaurantList) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            restaurantList.querySelectorAll('.restaurant-card').forEach(function(card) {
                const name = card.dataset.name || '';
                const desc = card.dataset.desc || '';
                const cuisines = card.dataset.cuisines || '';
                const match = !query || name.includes(query) || desc.includes(query) || cuisines.includes(query);
                card.classList.toggle('hidden-by-search', !match);
            });
        });
    }

    document.querySelectorAll('.cuisine-chip').forEach(function(chip) {
        chip.addEventListener('click', function() {
            document.querySelectorAll('.cuisine-chip').forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            const filter = this.dataset.filter || 'all';
            if (restaurantList) {
                restaurantList.querySelectorAll('.restaurant-card').forEach(function(card) {
                    if (filter === 'all') {
                        card.classList.remove('hidden-by-search');
                    } else {
                        const cuisines = card.dataset.cuisines || '';
                        card.classList.toggle('hidden-by-search', !cuisines.includes(filter));
                    }
                });
            }
        });
    });

    document.querySelectorAll('.filter-pill').forEach(function(pill) {
        pill.addEventListener('click', function() {
            document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
            this.classList.add('active');
        });
    });

    document.querySelectorAll('.category-tab').forEach(function(tab) {
        tab.addEventListener('click', function() {
            document.querySelectorAll('.category-tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            const target = this.dataset.target;
            document.querySelectorAll('.menu-category-section').forEach(function(section) {
                if (target === 'all') {
                    section.style.display = 'block';
                } else {
                    section.style.display = section.id === target ? 'block' : 'none';
                }
            });
        });
    });

    const locBar = document.getElementById('location-bar');
    if (locBar) {
        locBar.addEventListener('click', initGeolocation);
    }
});

function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

function updateLocationUI(city, area) {
    const cityEl = document.getElementById('loc-city');
    const areaEl = document.getElementById('loc-area');
    if (cityEl) cityEl.textContent = city || 'Unknown city';
    if (areaEl) areaEl.textContent = area || '';
}

function saveLocationToServer(lat, lng, city, area) {
    fetch('/accounts/save-location/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ lat, lng, city, area }),
    }).catch(function() {});
}

function reverseGeocode(lat, lng) {
    const url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat=' + lat + '&lon=' + lng + '&zoom=16&addressdetails=1';
    return fetch(url, {
        headers: { 'Accept': 'application/json' },
    }).then(function(r) { return r.json(); });
}

function initGeolocation() {
    const cityEl = document.getElementById('loc-city');
    if (!cityEl) return;

    if (!navigator.geolocation) {
        updateLocationUI('Location unavailable', 'Browser does not support GPS');
        return;
    }

    updateLocationUI('Detecting location...', 'Please allow access');

    navigator.geolocation.getCurrentPosition(
        function(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            reverseGeocode(lat, lng)
                .then(function(data) {
                    const addr = data.address || {};
                    const city = addr.city || addr.town || addr.village || addr.county || addr.state_district || 'Your City';
                    const area = addr.suburb || addr.neighbourhood || addr.road || addr.state || '';
                    const state = addr.state || '';
                    const cityDisplay = state ? city + ', ' + state : city;
                    updateLocationUI(cityDisplay, area);
                    saveLocationToServer(lat, lng, cityDisplay, area);
                })
                .catch(function() {
                    updateLocationUI('Location detected', lat.toFixed(2) + ', ' + lng.toFixed(2));
                    saveLocationToServer(lat, lng, 'GPS Location', lat.toFixed(4) + ', ' + lng.toFixed(4));
                });
        },
        function(err) {
            if (err.code === 1) {
                updateLocationUI('Pune, Maharashtra', 'Enable location for accurate results');
            } else {
                updateLocationUI('Pune, Maharashtra', 'Hinjewadi, Phase 1');
            }
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
    );
}
