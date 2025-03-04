import "./App.css";
import { Routes, Route } from "react-router";
import Login from "./pages/Login";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />}></Route>
      <Route path="/teste" element={<div>xululu</div>}></Route>
    </Routes>
  );
}

export default App;
