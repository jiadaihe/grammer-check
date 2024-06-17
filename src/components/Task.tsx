import React, { useState } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';
import { useNavigate } from 'react-router-dom';


const TaskPage: React.FC = () => {
  const { startRecording, stopRecording, mediaBlobUrl, clearBlobUrl, status, error } = useReactMediaRecorder({ audio: true });
  const navigate = useNavigate();
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [submissionId, setSubmissionId] = useState<number>(0);

  const handleStartRecording = () => {
    clearBlobUrl(); // Clear previous recording
    startRecording();
    console.log({mediaBlobUrl: mediaBlobUrl})

  };

  const handleStopRecording = () => {
    stopRecording();
    console.log({mediaBlobUrl: mediaBlobUrl})
  };

  const handlePlayRecording = () => {
    // Implement audio playback logic here
    console.log('Play recording');
  };

  const handleReRecord = () => {
    // Reset the audioBlob state
    setAudioBlob(null);
  };

  const handleSubmit = () => {
    // Send the audioBlob to the backend for processing
    console.log('Submitting audio:', audioBlob);
    // Implement navigation to FeedbackPage here
  };

  const handleUpload = async () => {
    if (mediaBlobUrl) {
      try {
        const blobResponse = await fetch(mediaBlobUrl);
        const filename = mediaBlobUrl.substring(mediaBlobUrl.indexOf(':3000/') + 6);
        const blob = await blobResponse.blob();

        // Create a FormData object and append the blob
        const formData = new FormData();
        formData.append('file', blob, `${filename}.wav`);

        // Send the formData to the backend
        console.log('sending to backend')
        const response = await fetch('http://localhost:8000/upload', {
          method: 'POST',
          body: formData,
          headers: {},
        });

        if (response.ok) {
          const data = await response.json()
          setSubmissionId(data.submissionId)
          navigate(`/feedback/${data.submissionId}`);
          console.log('File uploaded successfully');
        } else {
          console.error('File upload failed');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  return (
    <div>
      <h1>Simulation Task</h1>
      <p>Record an audio selling a healthcare service</p>
      <div>
        <button onClick={handleStartRecording} disabled={status === "recording"}>Start Recording</button>
        <button onClick={handleStopRecording} disabled={status !== "recording"}>Stop Recording</button>
        <button onClick={clearBlobUrl} disabled={!mediaBlobUrl}>Re-record</button>
        <button onClick={() => navigate('/')}>Back to Home</button>
      </div>
        {status === "recording" && <p>Recording in progress...</p>}
        {mediaBlobUrl && (
            <div>
            <h2>Recorded Audio</h2>
            <audio src={mediaBlobUrl} controls />
            <button onClick={handleUpload}>Upload Recording</button>
            </div>
        )}
        {error && error.includes("NotAllowedError") && (
            <p>Permission to access the microphone was denied.</p>
        )}
        {error && <p>Error: {error.toString()}</p>}
    </div>
  );
};

export default TaskPage;