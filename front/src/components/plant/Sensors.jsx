import { Accordion } from 'react-bootstrap';
import useAxiosPrivate from '../../hooks/useAxiosPrivate';
import {useState, useEffect} from 'react';
import Spinner from 'react-bootstrap/Spinner';
import Sensor from './Sensor';
import {useTranslation} from 'react-i18next';


const Sensors = ({plantId}) => {
    const {t} = useTranslation();
    const axiosPrivate = useAxiosPrivate();
    const [sensors, setSensors] = useState();

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();
        const getSensors = async () => {
            try {
                const response = await axiosPrivate.get('/sensors', {
                    signal: controller.signal
                });
                isMounted && setSensors(response.data?.msg?.sensors);
            } catch(e) {
                console.error(e);
            }
        }

        getSensors();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, []);

    return (
        <Accordion flush alwaysOpen defaultActiveKey="0">
            {
                sensors && sensors.length > 0 
                ?
                sensors.filter(x => x.plants?.includes(plantId))
                    .map((sensor, index) => {
                        return (
                            <Accordion.Item eventKey={String(index)}>
                            <Accordion.Header>{`${t("sensor")} - ${sensor?.type} - ${sensor?._id}`}</Accordion.Header>
                            <Accordion.Body>
                                <Sensor sensor={sensor} plantId={plantId}/>
                            </Accordion.Body>
                            </Accordion.Item>
                        );
                    })
                :
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            }
        </Accordion>
    );
}

export default Sensors;