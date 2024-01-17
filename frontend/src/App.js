import {
  BrowserRouter as Router,
  Route,
  Routes
} from "react-router-dom";

import Nav from './Components/Nav';
import Home from './Pages/Home/Home';
import Notification from "./Pages/Notification/Notification.jsx";
import Auth from "./Pages/Authentication/Auth/Auth.jsx";
import SignInAsPolice from "./Pages/Authentication/signInAsPolice/SignInAsPolice.jsx";
import SignInAsCameraOwner from "./Pages/Authentication/signInAsCameraOwner/SignInAsCameraOwner.jsx";
import ResponseForm from "./Pages/Notification/NotiResponse.jsx";
import MapComponent from "./Pages/Notification/Map.jsx";

function App() {
  return (
   
    <Router>
      <Nav/>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/notification" element={<Notification />} />
        
        <Route path="/authentication" element={<Auth />} />
        <Route path="/authentication/police" element={<SignInAsPolice />} />
        <Route path="/authentication/camera-owner" element={<SignInAsCameraOwner />} />
        <Route path="/noti-response" element={<ResponseForm />} />
        <Route path="/livemap" element={<MapComponent />} />
        {/* <Route path="about" element={<h1>About</h1>} />
        <Route path="*" element={<h1>Not Found</h1>} /> */}
      </Routes>
    </Router>
  );
}

export default App;
