import React,{useState,useEffect} from "react";
import "./Notification.css";
import axios from "axios";

import MapComponent from "./Map";

const Notification = () => {
    const [data, setData] = useState([]);
    const [cord, setCord] = useState([0, 0]);
    
    const viewMap = (cord) => {
        console.log(cord);
        setCord(cord);
        
    }
    
    useEffect( () => {
        // Fetch data when the component mounts
        axios.get('http://127.0.0.1:5000/get_cameraOwner')
            .then(response => {
                console.log(response.data);
                setData(response.data);
                // setCord(response.data["Latitude"], response.data["Longitude"]);
                // console.log(response.data["Location"]);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
        
    }, []);
    return (
        <>
            <div className="notification-content">
                <h2>Notification Content</h2>
            </div>
            <div>
                {data.map(item => (
                <div>
            <div className="row">
                <div>
                    <h2>{item.name}</h2>
                    <p>{item.email}</p>
                    <p>{item.Contact}</p>      
                    <p>{item.Address}</p>
                    <p>{item.resolution}</p>     
                    <p>{item.radius}</p>
                    <p>{item.powerning}</p>          
                </div>
                <div className="buttons">
                    <div className="button detail" onClick={()=>viewDetails('1')}>View details</div>
                    <div className="button ignore">Ignore</div>
                    <div className="button video" onClick={() => viewDetails('1')}>Video</div>
                    <div className="button live" onClick={() =>  viewMap(item.Location)}>Live</div>
                    <div className="button accept">Accept</div>
                </div>
            </div>

            <div className="row">
                <div>
                    <h2>User 2</h2>
                    <p>Information of user 2.</p>
                </div>
                <div className="buttons">
                    <div className="button detail" onclick={()=>viewDetails('2')}>View details</div>
                    <div className="button ignore">Ignore</div>
                    <div className="button video" onclick={() => viewVideo('2') }>Video</div>
                    <div className="button live">Live</div>
                    <div className="button accept">Accept</div>
                </div>
            </div>

            <div id="detailsModal" className="modal">
                <div className="modal-content">
                    <span className="close" onclick={()=>closeModal()}>&times;</span>
                    <h2>Details</h2>
                    <table id="detailsTable">
                        
                    </table>
                    <video id="videoPlayer" controls style={{ "display": "none"}}>
                        Your browser does not support the video tag.
                    </video>
                </div>
            </div>

            <div id="customProgressBar" onClick={(event)=>seek(event)}>
                <div id="progress"></div>
                <div id="marker"></div>
            </div>
                    </div>
                   
                ))}
                <div>
                    <MapComponent latitude={cord[0]} longitude={cord[1]} />
                </div>
            </div>
        </>
    )
}

function viewDetails(key) {
    // Fetch data from data_storage
   
}

// Function to open the video modal and play the video
function viewVideo(key) {
    // Fetch video path from path
   
}

// Function to close the details modal
function closeModal() {
    var modal = document.getElementById('detailsModal');
    modal.style.display = 'none';

    // Pause the video when the modal is closed
    document.getElementById('videoPlayer').pause();

    // Hide the custom progress bar with marker
    document.getElementById('customProgressBar').style.display = 'none';
}

// Close the modal if the user clicks outside of it
window.onclick = function (event) {
    var modal = document.getElementById('detailsModal');
    if (event.target == modal) {
        modal.style.display = 'none';

        // Pause the video when the modal is closed
        document.getElementById('videoPlayer').pause();

        // Hide the custom progress bar with marker
        document.getElementById('customProgressBar').style.display = 'none';
    }
}

// Custom progress bar and marker logic
var video = document.getElementById('videoPlayer');
var progressBar = document.getElementById('customProgressBar');
var progress = document.getElementById('progress');
var marker = document.getElementById('marker');


function updateProgressBar() {
    var value = (video.currentTime / video.duration) * 100;
    progress.style.width = value + '%';
    marker.style.left = ((3 / video.duration) * progressBar.offsetWidth) + "px";
}

function seek(event) {
    var rect = progressBar.getBoundingClientRect();
    var x = event.clientX - rect.left;
    var percentage = (x / progressBar.clientWidth) * 100;
    var seekTime = (percentage / 100) * video.duration;
    video.currentTime = seekTime;
}

// video.addEventListener('timeupdate', updateProgressBar);

export default Notification;