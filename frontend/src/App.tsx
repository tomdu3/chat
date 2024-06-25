import Home from "./pages/Home";
import {
  createBrowserRouter,
  Route,
  RouterProvider,
  createRoutesFromElements,
} from "react-router-dom";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Home />} />
    </Route>,
  ),
);

const App: React.FC = () => {
  return <RouterProvider router={router} />;
};

export default App;
