// frontend/src/components/PostList.jsx
import React, { useState, useEffect } from 'react';
import { getAllPosts, publishPost } from '../services/api';

function PostList() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [publishingId, setPublishingId] = useState(null);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const fetchedPosts = await getAllPosts();
        setPosts(fetchedPosts);
      } catch (error) {
        console.error('Error fetching posts:', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchPosts();
  }, []);

  const handlePublish = async (postId) => {
    setPublishingId(postId);
    setMessage({ type: '', text: '' });

    try {
      await publishPost(postId);
      setMessage({ type: 'success', text: 'Post published successfully to Twitter!' });
    } catch (error) {
      setMessage({ type: 'error', text: error.message });
    } finally {
      setPublishingId(null);
    }
  };

  const getPlatformEmoji = (platform) => {
    const emojis = {
      twitter: '🐦',
      linkedin: '💼',
      instagram: '📸'
    };
    return emojis[platform] || '📱';
  };

  const getToneEmoji = (tone) => {
    const emojis = {
      professional: '👔',
      funny: '😄',
      witty: '💡',
      casual: '🙂',
      inspirational: '🌟'
    };
    return emojis[tone] || '✍️';
  };

  return (
    <div className="post-container" style={{ maxWidth: '700px', margin: '0 auto' }}>
      <h2>📚 Saved Posts</h2>

      {message.text && (
        <div className={message.type === 'success' ? 'success-message' : 'error-message'}>
          {message.type === 'success' ? '✅' : '❌'} {message.text}
        </div>
      )}

      {isLoading ? (
        <div style={{
          textAlign: 'center',
          padding: '60px',
          color: '#94a3b8'
        }}>
          <span className="loading" style={{ fontSize: '2rem' }}>⏳</span>
          <p style={{ marginTop: '16px' }}>Loading posts...</p>
        </div>
      ) : posts.length > 0 ? (
        posts.map((post) => (
          <div key={post.id} className="post-item">
            <h4>
              {getPlatformEmoji(post.platform)} {post.platform.charAt(0).toUpperCase() + post.platform.slice(1)}
              &nbsp;•&nbsp;
              {getToneEmoji(post.tone)} {post.tone.charAt(0).toUpperCase() + post.tone.slice(1)}
            </h4>

            <p><strong>Prompt:</strong> {post.prompt}</p>
            <p style={{ whiteSpace: 'pre-wrap' }}><strong>Generated Content:</strong> {post.generated_content}</p>

            <small>
              🕐 {new Date(post.created_at).toLocaleString()}
            </small>

            <div style={{ marginTop: '16px' }}>
              <button
                onClick={() => handlePublish(post.id)}
                disabled={publishingId === post.id}
                style={{
                  background: post.platform === 'twitter'
                    ? 'linear-gradient(135deg, #1da1f2, #0d8ecf)'
                    : undefined
                }}
              >
                {publishingId === post.id ? (
                  <><span className="loading">⏳</span> Posting...</>
                ) : (
                  <>🐦 Post to Twitter</>
                )}
              </button>
            </div>
          </div>
        ))
      ) : (
        <div style={{
          textAlign: 'center',
          padding: '60px',
          background: 'rgba(30, 41, 59, 0.5)',
          borderRadius: '16px',
          border: '1px dashed rgba(148, 163, 184, 0.3)'
        }}>
          <span style={{ fontSize: '3rem' }}>📝</span>
          <p style={{ color: '#94a3b8', marginTop: '16px' }}>
            No posts saved yet. Create one above!
          </p>
        </div>
      )}
    </div>
  );
}

export default PostList;