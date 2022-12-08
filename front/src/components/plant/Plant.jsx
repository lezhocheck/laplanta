import {useState, useEffect} from 'react';
import { useParams } from 'react-router-dom';
import useAxiosPrivate from '../../hooks/useAxiosPrivate';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import ListGroup from 'react-bootstrap/ListGroup';
import Col from 'react-bootstrap/Col';
import {AiOutlineInfoCircle, AiOutlineCalendar} from 'react-icons/ai';
import {MdDriveFileRenameOutline} from 'react-icons/md';
import {RiPlantLine} from 'react-icons/ri';
import {useNavigate} from 'react-router-dom';
import Sensors from './Sensors';
import Button from 'react-bootstrap/Button';
import {useTranslation} from 'react-i18next';

const Plant = () => {
    const {t} = useTranslation();
    const axiosPrivate = useAxiosPrivate();
    const [plant, setPlant] = useState();
    const {id} = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();
        const getPlant = async () => {
            try {
                const response = await axiosPrivate.get(`/plant/${id}`, {
                    signal: controller.signal
                });
                isMounted && setPlant(response.data?.msg?.plant);
            } catch(e) {
                if (e.response?.status === 400) {
                    navigate('/missing');
                    return;
                }
                console.error(e);
            }
        }

        getPlant();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, []);


    return (
        <div className='bg-light'>
            <Container className="py-5">
                <Row>
                    <Col>
                        <ListGroup>
                            <ListGroup.Item className="text-center">
                                <RiPlantLine size={200} className='text-secondary'/>
                                <p className="mb-1">{plant?.name}</p>
                                <p className="text-muted mb-4">{plant?._id}</p>
                            </ListGroup.Item>
                        </ListGroup>
                        <br/>
                        <ListGroup>
                            
                        </ListGroup>
                    </Col>
                    <Col lg="8">
                        <ListGroup>
                            <ListGroup.Item>
                                <Row>
                                    <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                                        <MdDriveFileRenameOutline size={20}/>
                                        <span className="p">{t("plant_name")}</span>
                                    </Col>
                                    <Col sm="9" className="d-flex justify-content-start align-items-center">
                                        <span className="p text-muted">{plant?.name}</span>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                                        <AiOutlineInfoCircle size={20}/>
                                        <span className="p">{t("description")}</span>
                                    </Col>
                                    <Col sm="9" className="d-flex justify-content-start align-items-center">
                                        <span className="p text-muted">{plant?.description}</span>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col sm="3" className="d-flex justify-content-start align-items-center gap-1">
                                        <AiOutlineCalendar size={20}/>
                                        <span className="p">{t("added_date")}</span>
                                    </Col>
                                    <Col sm="9" className="d-flex justify-content-start align-items-center">
                                        <span className="p text-muted">{plant?.added_date}</span>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <div className="d-flex justify-content-end mb-2 gap-3">
                                    <Button variant="primary" disabled>{t("edit")}</Button>
                                    <Button variant="outline-primary" disabled>{t("delete")}</Button>
                                </div>
                            </ListGroup.Item>
                        </ListGroup>
                        <br/>
                        <Row>
                            <Col md="6">
                               
                            </Col>
                            <Col md="6">
                                
                            </Col>
                        </Row>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <h1>{t("sensors")}</h1>
                        <br/>
                        <Sensors plantId={id}/>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}

export default Plant;