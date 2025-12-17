// frontend/src/components/PostForm.jsx

import React, { useState } from 'react';
import { generatePost } from '../services/api';

function PostForm() {
  // State for the form inputs
  const [prompt, setPrompt] = useState('');
  const [platform, setPlatform] = useState('linkedin');
  const [tone, setTone] = useState('professional');

  // State for the result and loading status
  const [generatedContent, setGeneratedContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setGeneratedContent('');
    setError('');

    try {
      const postData = { prompt, platform, tone };
      const result = await generatePost(postData);
      setGeneratedContent(result.generated_content);
    } catch (error) {
      setError('Failed to generate post. Please check your API connection and try again.');
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '700px', margin: '0 auto' }}>
      <h2>✨ Generate a New Post</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '20px' }}>
          <label htmlFor="prompt">Your Idea</label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows="4"
            placeholder="Describe what you want to post about..."
            required
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' }}>
          <div>
            <label htmlFor="platform">Platform</label>
            <select
              id="platform"
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
            >
              <option value="twitter">🐦 Twitter</option>
              <option value="linkedin">💼 LinkedIn</option>
              <option value="instagram">📸 Instagram</option>
            </select>
          </div>

          <div>
            <label htmlFor="tone">Tone</label>
            <select
              id="tone"
              value={tone}
              onChange={(e) => setTone(e.target.value)}
            >
              <option value="professional">👔 Professional</option>
              <option value="funny">😄 Funny</option>
              <option value="witty">💡 Witty</option>
              <option value="casual">🙂 Casual</option>
              <option value="inspirational">🌟 Inspirational</option>
            </select>
          </div>
        </div>

        <button type="submit" disabled={isLoading}>
          {isLoading ? (
            <>
              <span className="loading">⏳</span> Generating...
            </>
          ) : (
            <>🚀 Generate Post</>
          )}
        </button>
      </form>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {generatedContent && (
        <div style={{
          marginTop: '24px',
          padding: '24px',
          background: 'rgba(30, 41, 59, 0.8)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(148, 163, 184, 0.2)',
          borderRadius: '16px'
        }}>
          <h3 style={{
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            marginBottom: '16px'
          }}>
            ✅ Generated Post
          </h3>
          <p style={{
            color: '#f8fafc',
            lineHeight: '1.8',
            fontSize: '1rem',
            whiteSpace: 'pre-wrap'
          }}>
            {generatedContent}
          </p>
        </div>
      )}
    </div>
  );
}

export default PostForm;