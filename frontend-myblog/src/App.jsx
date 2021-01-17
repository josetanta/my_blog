import HomeScreen from "./screens/HomeScreen";
import { BrowserRouter, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Route path="/" component={HomeScreen} />
      </BrowserRouter>
    </div>
  );
}

export default App;
