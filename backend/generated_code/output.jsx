import React, { useState, useEffect } from 'react';

const App = () => {
    const [inputFields, setInputFields] = useState([]);
    const [inputValues, setInputValues] = useState({});
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchMetadata = async () => {
            setLoading(true);
            setError(null);
            try {
                const response = await fetch('http://127.0.0.1:8000/metadata');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                if (data && Array.isArray(data.input_fields)) {
                    setInputFields(data.input_fields);
                    const initialInputValues = {};
                    data.input_fields.forEach(field => {
                        initialInputValues[field] = '';
                    });
                    setInputValues(initialInputValues);
                } else {
                    setError('Invalid metadata response format.');
                }
            } catch (e) {
                setError('Failed to fetch input fields metadata.');
                console.error("Metadata fetch error:", e);
            } finally {
                setLoading(false);
            }
        };

        fetchMetadata();
    }, []);

    const handleInputChange = (event) => {
        setInputValues({ ...inputValues, [event.target.name]: event.target.value });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError(null);
        setPrediction(null);

        try {
            const numericInputValues = {};
            for (const key in inputValues) {
                numericInputValues[key] = parseFloat(inputValues[key]);
                if (isNaN(numericInputValues[key])) {
                    throw new Error(`Invalid input for field: ${key}. Please enter a number.`);
                }
            }

            const response = await fetch('http://127.0.0.1:8000/predict/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(numericInputValues),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Prediction request failed: ${response.status} - ${errorData.detail || 'Unknown error'}`);
            }

            const data = await response.json();
            setPrediction(data);
        } catch (e) {
            setError(e.message);
            console.error("Prediction error:", e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>BMI Prediction</h1>
            {error && <p style={{ color: 'red' }}>Error: {error}</p>}
            {loading && <p>Loading...</p>}

            <form onSubmit={handleSubmit}>
                {inputFields.map((field) => (
                    <div key={field}>
                        <label htmlFor={field}>{field}: </label>
                        <input
                            type="number"
                            id={field}
                            name={field}
                            value={inputValues[field] || ''}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                ))}
                <button type="submit" disabled={loading}>Predict</button>
            </form>

            {prediction && (
                <div>
                    <h2>Prediction Result:</h2>
                    <p>Input Data: {JSON.stringify(prediction.input)}</p>
                    <p>Predicted BMI Class: {prediction.prediction}</p>
                </div>
            )}
        </div>
    );
};

export default App;