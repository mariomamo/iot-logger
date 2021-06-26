import './App.css';
import Chat from './components/Chat/chat';

function App() {
  const root = document.getElementById('root');
  return (
    <Chat url={root.getAttribute("url")} port={root.getAttribute("port")}/>
  );
}

export default App;
