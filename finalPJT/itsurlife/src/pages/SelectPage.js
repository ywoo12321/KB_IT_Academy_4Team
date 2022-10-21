import Navbar from "../components/Navbar";
import styled from "@emotion/styled";
import theme from "../styles/theme";
import Btn from "../components/Btn";
import axios from "axios";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const SelectPage = () => {
  const [locationInfo, setlocationInfo] = useState([]);
  const [clicked, setClicked] = useState([]);

  const handleClick = event => {
    const item = event.target;
    if (clicked.length >= 5) {
      return;
    }
    item.setAttribute(clicked, true);
    setClicked([...item]);
  };

  const fetchlocation = async () => {
    //근처 지역 숙소 정보 받아오기
    const response = await axios.get("https://kaybe-wgkwk.run.goorm.io/lodgings/random/");
    await console.log(response.data);
    setlocationInfo(response.data);
  };
  useEffect(() => {
    fetchlocation();
  }, []);
  return (
    <>
      <Navbar />
      <Container>
        <SelectBox>
          <div>
            <TitleName>
              당신의 취향을 골라보세요
              <TitleSmallName>(0~5개 선택 가능)</TitleSmallName>
            </TitleName>
          </div>
          <ImgContainer>
            {Object.keys(locationInfo).map(lodging => {
              return (
                <ImgBox key={lodging} onClick={handleClick}>
                  <img src={locationInfo[lodging].src} alt={lodging.name} />
                </ImgBox>
              );
            })}
          </ImgContainer>
          <BtnBox>
            <Link to="/signup">
              <Btn>이전</Btn>
            </Link>
            <Btn>완료</Btn>
          </BtnBox>
        </SelectBox>
      </Container>
    </>
  );
};

export default SelectPage;

const Container = styled.div`
  height: 2247px;
`;

const SelectBox = styled.div`
  width: 93%;
  height: 90%;
  margin: 0 auto;
  margin-top: 58px;

  box-shadow: 0px 6px 4px rgba(0, 0, 0, 0.1), inset 0px 8px 18px 8px rgba(82, 79, 74, 0.1);
  border-radius: 40px;
`;

const TitleName = styled.h1`
  font-family: ${theme.font_family.T};
  font-size: ${theme.font_size.h1};
  margin-left: 670px;
  padding-top: 65px;
  opacity: 1;
  color: black;
`;

const TitleSmallName = styled.span`
  font-family: ${theme.font_family.B};
  padding-left: 20px;
  font-size: ${theme.font_size.subtitle1};
  line-height: 25px;
  color: red;
`;

const ImgContainer = styled.div`
  height: 80%;
  padding-top: 14px;
  margin: 0 auto;
  text-align: center;
`;

const ImgBox = styled.div`
  display: inline-block;
  width: 361px;
  height: 241px;
  position: relative;
  margin-left: 26px;
  margin-right: 26px;
  margin-top: 45px;
  margin-bottom: 45px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 25px;
  overflow: hidden;
  border: ${({ clicked }) => (clicked ? "3px solid black" : "none")};
  & > img {
    width: 100%;
    height: 100%;
  }
`;

const BtnBox = styled.div`
  text-align: center;
  margin-top: 100px;
  & > button {
    margin-left: 70px;
    margin-right: 70px;
  }
`;
