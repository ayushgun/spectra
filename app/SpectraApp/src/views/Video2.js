import React from 'react';
import {
  ImageBackground,
  StyleSheet,
  View,
  Button
} from 'react-native';
import { Text } from 'react-native-paper';
import { useEffect, useRef, useState } from 'react';
import { shareAsync } from 'expo-sharing';
import * as MediaLibrary from 'expo-media-library';
import { StatusBar } from 'expo-status-bar';
import { FAB } from 'react-native-paper';
import { theme } from '../core/theme';
import { Camera, NoCameraDeviceError, useCameraDevice, useCameraPermission, useTensorflow } from 'react-native-vision-camera';
// import { Logs } from 'expo'
import { DetectedObject, detectObjects, FrameProcessorConfig } from 'vision-camera-realtime-object-detection';
import { runOnJS } from 'react-native-reanimated';

// Logs.enableExpoCliLogging()

const Video2 = ({ navigation }) => {
  // const camera = useRef();
  const camera = useRef();

  const { hasPermission, requestPermission } = useCameraPermission();
  const device = useCameraDevice('back');

  const [objects, setObjects] = useState([]);

  const frameProcessorConfig: FrameProcessorConfig = {
    modelFile: require('../../assets/model/yolov8n_float32.tflite'), // <!-- name and extension of your model
    scoreThreshold: 0.5,
  };

  const frameProcessor = useFrameProcessor((frame) => {
    'worklet';

    const detectedObjects = detectObjects(frame, frameProcessorConfig);
    runOnJS(setObjects)(
      detectedObjects.map((obj) => ({
        ...obj,
        top: obj.top * windowDimensions.height,
        left: obj.left * windowDimensions.width,
        width: obj.width * windowDimensions.width,
        height: obj.height * windowDimensions.height,
      }))
    );
  }, []);

  // useEffect(() => {
  //   requestPermission();
  //   const checkPermission = async () => {
  //     const status = await Camera.getCameraPermissionStatus();
  //     setPermissionsAuth(status)
  //     if (status !== 'granted') {
  //       return null
  //     } else if (status === 'granted') {
  //       setShowCamera(true)
  //     }
  //   };

  //   checkPermission();
  // }, []);
  if (hasPermission === false) {
    return (
      <View style={styles.container}>
        <Text>Permission for camera not granted. Please change this in settings.</Text>
        <Button title="Request Permission" onPress={requestPermission} />
      </View>
    )
  }

  if (device == null) return <NoCameraDeviceError />
  return (
    <>
      {/* <FAB
        icon="menu"
        style={styles.fab}
        onPress={() => {
          navigation.navigate('Settings');
          // console.log('Settings');
        }}
      /> */}
      <Camera
        ref={camera}
        style={StyleSheet.absoluteFill}
        resizeMode='cover'
        device={device}
        isActive={true}
        frameProcessorFps={5}
        frameProcessor={frameProcessor}
      >
        {objects?.map(
          (
            { top, left, width, height, labels }: DetectedObject,
            index: number
          ) => (
            <View
              key={`${index}`}
              style={[styles.detectionFrame, { top, left, width, height }]}
            >
              <Text style={styles.detectionFrameLabel}>
                {labels
                  .map((label) => `${label.label} (${label.confidence})`)
                  .join(',')}
              </Text>
            </View>
          )
        )}
      </Camera>
        {/* <Text>Future implementation of Toast.</Text> */}
        {/* <StatusBar style="auto" /> */}
      <FAB
        icon="menu"
        style={styles.fab}
        onPress={() => {
          navigation.navigate('Settings');
          // console.log('Settings');
        }}
      />
      
    </>
    
    
  )
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    // flex: 1,
    // alignItems: 'center',
    // justifyContent: 'center',
  },
  // fab: {
  //   // alignSelf: 'flex-start',
  //   // left: 20,
  //   // top: 0,
  //   // marginTop: 20,
  //   // marginBottom: 650,
  //   opacity: 1,
  //   width: 'auto',
  //   height: 'auto',
  // },
  fab: {
    position: 'absolute',
    margin: 20,
    justifyContent: 'center',
    alignItems: 'center',
    // top: 20,
    // left: 20,
    right: 20,
    bottom: 20,
    width: 70,  // Explicit width
    height: 70, // Explicit height
    borderRadius: 28, // For circular shape
  },
  detectionFrame: {
    position: 'absolute',
    borderWidth: 1,
    borderColor: '#00ff00',
    zIndex: 9,
  },
  detectionFrameLabel: {
    backgroundColor: 'rgba(0, 255, 0, 0.25)',
  },
});

export default Video2