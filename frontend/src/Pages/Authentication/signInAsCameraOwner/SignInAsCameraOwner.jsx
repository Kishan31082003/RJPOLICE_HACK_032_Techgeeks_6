import { useState } from 'react';
import axios from 'axios';
import "./signInAsCameraOwner.css";
import L from 'leaflet';


const SignInAsCameraOwner = () => {

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        Contact: '',
        Location: [0,0],
        Address: '',
        resolution: '',
        radius: '',
        powerning: '',
    });
    
    const handleInputChange = (e) => {
        e.preventDefault();

        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const submitForm = async () => {
        // Convert form data to JSON
        const jsonData = JSON.stringify(formData);

        // Send JSON data to the server (replace 'your-server-endpoint' with the actual server endpoint)
        try {
            const response = await axios.post('http://127.0.0.1:5000/admin/cameraOwner', jsonData, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = response.data;
            console.log('Success:', data);
            setFormData({
                name: '',
                email: '',
                Contact: '',
                Location: [0,0],
                Address: '',
                resolution: '',
                radius: '',
                powerning: '',});
            
            // Handle success response from the server
        } catch (error) {
            console.error('Error:', error);
            // Handle error
        }
    };
    
    const handleShareLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    const userLocation = [latitude, longitude];

                    
                    console.log('User Location:', userLocation);
                    setFormData({
                        ...formData,
                        Location: userLocation,
                    });
                   
                },
                (error) => {
                    console.error('Error getting location:', error.message);
                }
            );
        } else {
            console.error('Geolocation is not supported by your browser');
        }
    };

    return (
        <div className='sigin_as_cameraowner'>
            <h2 className='sigin_as_cameraowner_heading'> Contributor Details</h2>
            <form className='sigin_as_cameraowner_form'>
                <label htmlFor="name">Organization/Owner Name:</label>
                <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                />

                <label htmlFor="email">Email:</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                />

                <label htmlFor="Contact">Contact No.:</label>
                <input
                    type="number"
                    id="Contact"
                    name="Contact"
                    value={formData.Contact}
                    onChange={handleInputChange}
                    required
                />

                <label htmlFor="Location">Location:</label>
                <button onClick={handleShareLocation}>Share Location </button>

                <label htmlFor="Address">Address:</label>
                <input
                    type="text"
                    id="address"
                    name="Address"
                    value={formData.Address}
                    onChange={handleInputChange}
                    required
                />

                

                <label htmlFor="resolution">Resolution:</label>
                <input
                    type="text"
                    id="resolution"
                    name="resolution"
                    value={formData.resolution}
                    onChange={handleInputChange}
                    required
                />

                <label htmlFor="radius">Camera Radius:</label>
                <input
                    type="number"
                    id="radius"
                    name="radius"
                    value={formData.radius}
                    onChange={handleInputChange}
                    required
                />

                <label htmlFor="powerning">Powerning line/Electricity phase:</label>
                <input
                    type="text"
                    id="powerning"
                    name="powerning"
                    value={formData.powerning}
                    onChange={handleInputChange}
                    required
                />

                <button className="sigin_as_cameraowner_button" type="button" onClick={submitForm}>
                    Submit
                </button>
            </form>
        </div>
    );
};

export default SignInAsCameraOwner;
