import React from 'react';

const ResponseForm = () => {
    return (
        <div>
            <h2>Record Response</h2>

            <form action="submit_response.php" method="post">
                <label for="mobileNumber">Mobile Number:</label>
                <input type="text" id="mobileNumber" name="mobileNumber" readonly />

                    <label for="userNumber">User Number:</label>
                    <input type="text" id="userNumber" name="userNumber" readonly />

                        <label for="password">Password:</label>
                        <input type="password" id="password" name="password" readonly />

                            <label for="qrCode">QR Code:</label>
                            <input type="file" id="qrCode" name="qrCode" readonly />

                                <label for="response">Response:</label>
                                <textarea id="response" name="response" required></textarea>

                                <input type="submit" value="Submit Response" />
            </form>
        </div>
    );
};

export default ResponseForm;
