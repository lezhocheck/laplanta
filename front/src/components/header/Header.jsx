import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import {RiPlantLine} from 'react-icons/ri';
import {FaUserAlt, FaLanguage} from 'react-icons/fa';
import {useTranslation} from 'react-i18next';

export default function Header() {
    const {t, i18n} = useTranslation();

    function changeLanguage(language) {
        i18n.changeLanguage(language);
    }

    return (
        <Navbar sticky="top" bg="dark" variant="dark">
            <Container>
                <Navbar.Brand href="#home">
                    <RiPlantLine size={40}/> Laplanta
                </Navbar.Brand>
                <Nav className="ml-auto">
                    <NavDropdown title={
                        <span><FaLanguage size={30}/> {t("lang")}</span>
                        } onSelect={changeLanguage}>
                        <NavDropdown.Item eventKey="en">English</NavDropdown.Item>
                        <NavDropdown.Item eventKey="ua">Українська</NavDropdown.Item>
                    </NavDropdown>
                    <Nav.Link href="#home"><FaUserAlt size={18}/> {t("profile")}</Nav.Link>
                </Nav>
            </Container>
        </Navbar>
    );
}