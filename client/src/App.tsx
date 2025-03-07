import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MyForm from "./pages/Form";  // Your upload page
import ResultsPage from "./pages/Results";  // New results page

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MyForm />} />
        <Route path="/results" element={<ResultsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
