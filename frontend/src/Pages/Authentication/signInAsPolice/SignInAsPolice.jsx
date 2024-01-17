
import React, { useState,useEffect } from 'react';
import L from 'leaflet';

import "./signInAsPolice.css";
import 'leaflet/dist/leaflet.css';

const SignInAsPolice = () => {
    const [name, setName] = useState('');
    const [location, setLocation] = useState('');
    const [password, setPassword] = useState('');
    const loginPolice = (event) => {
        event.preventDefault();

        // Perform validation and login logic here
        if (name && location && password) {
            alert(`Police login successful!\nName: ${name}\nLocation: ${location}`);
            // Redirect or perform further actions after successful login
            // For React, you might want to use React Router for navigation.
        } else {
            alert('Please enter valid credentials.');
        }
    };

    const handleLocationInputChange = (event) => {
        const query = event.target.value;

        // Use OpenMap API to get location suggestions
        // fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`)
        //     .then(response => response.json())
        //     .then(data => {
        //         // Assume the first result is the best match
        //         if (data && data.length > 0) {
        //             const result = data[0];
        //             const lat = result.lat;
        //             const lon = result.lon;
        //             // Use Leaflet to set the map view
        //             // map.setView([lat, lon], 13);
        //         }
        //     })
        //     .catch(error => console.error('Error fetching location suggestions:', error));
    };

    // Initialize Leaflet map with the OpenMap API for location suggestions
    // useEffect(() => {
    //     // Leaflet map initialization code here
    //     const map = L.map('map').setView([0, 0], 1);
    //     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //         attribution: '© OpenMapTiles'
    //     }).addTo(map);
    // }, []); // Empty dependency array to ensure it runs only once after mount


    return (
        <div className='sigin_as_police'>
            <div id="header">
                {/* Assuming you have a public/logo/logo.png file */}
                <img id="logo" src={process.env.PUBLIC_URL + '/logo/logo.png'} alt="Logo" />
                <h2>Police Login</h2>
            </div>
            <div id="login-container">
                <form onSubmit={loginPolice}>
                    <label htmlFor="name">Name:</label>
                    <input type="text" id="name" name="name" value={name} onChange={(e) => setName(e.target.value)} required />

                    {/* <label htmlFor="location">Location:</label>
                    <input type="text" id="location" name="location" value={location} onChange={(e) => setLocation(e.target.value)} required onInput={handleLocationInputChange} /> */}

                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} required />

                    <button className='sigin_as_police_button' type="submit">Login</button>
                </form>
            </div>

            {/* Map container */}
            <div id="map" style={{ height: '300px', width: '100%' }}></div>
        </div>
    );
};

export default SignInAsPolice;
