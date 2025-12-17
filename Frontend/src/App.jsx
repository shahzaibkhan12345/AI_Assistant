// frontend/src/App.jsx
import PostForm from './components/PostForm';
import PostList from './components/PostList';

function App() {
  return (
    <div>
      <header>
        <h1>🤖 AI Social Media Assistant</h1>
      </header>
      <main>
        <PostForm />
        <hr />
        <PostList />
      </main>
    </div>
  )
}

export default App;