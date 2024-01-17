import React from "react"
import { Link } from "react-router-dom";
import "./Auth.css";




const Auth = () => {
    const signInAsPolice = () => {
        // Redirect or perform actions for Police sign-in
        // Replace the following line with the actual URL for the Police sign-in page
        window.location.href = "/authentication/police";
    };

    const signInAsCameraOwner = () => {
        // Redirect or perform actions for Camera Owner sign-in
        // Replace the following line with the actual URL for the Camera Owner sign-in page
        window.location.href = "/authentication/camera-owner";
    };

    const signUpAsCameraOwner = () => {
        // Redirect or perform actions for Camera Owner sign-up
        // Replace the following line with the actual URL for the Camera Owner sign-up page
        window.location.href = "/authentication";
    };

    return (
        <div className="auth">
            <div className="auth_container">
                <h2>Choose Your Sign-In Option</h2>
                <button className="auth_button" onClick={signInAsPolice}>Sign In as Police Administrator</button>
                <button className="auth_button"  onClick={signInAsCameraOwner}>Sign In as Camera Contributor</button>
                <button className="auth_button"  onClick={signUpAsCameraOwner}>Create new Account</button>
            </div>
        </div>
    );
};

export default Auth;
