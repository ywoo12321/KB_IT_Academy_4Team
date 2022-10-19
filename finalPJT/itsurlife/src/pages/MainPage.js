import Footer from "../components/Footer";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import axios from "axios";

const MainPage = () => {
  const [lodgingInfo, setLodgingInfo] = useState([]);
  const fetchData = async () => {
    const response = await axios.get(
      "https://2bd94f30-be46-4031-b0dc-c5cc936e66e4.mock.pstmn.io/v1/home",
    );
    await console.log(response.data);
    setLodgingInfo(response.data);
  };
  useEffect(() => {
    fetchData();
  }, []);
  return (
    <>
      <NavBar />
      {lodgingInfo.map(lodging => (
        <div key={lodging.id}>
          <div>{lodging.name}</div>
          <div>{lodging.location}</div>
        </div>
      ))}
      <Footer />
    </>
  );
};

export default MainPage;
