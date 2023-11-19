import React from 'react';
import {
    ImageBackground,
    StyleSheet,
    View,
  } from 'react-native';
import { Text } from 'react-native-paper';
import { useEffect, useRef, useState } from 'react';
import { Camera } from 'expo-camera';
import { shareAsync } from 'expo-sharing';
import * as MediaLibrary from 'expo-media-library';
import { StatusBar } from 'expo-status-bar';
import { FAB } from 'react-native-paper';
import { theme } from './core/theme';
import { Audio } from 'expo-av';
import {Button} from 'react-native'



export default function Video({navigation}) {
    let cameraRef = useRef();
    const [hasCameraPermission, setHasCameraPermission] = useState();
    const [hasMediaLibraryPermission, setHasMediaLibraryPermission] = useState();
    const [recording, setRecording] = React.useState();

    async function startRecording() {
      try {
        console.log('Requesting permissions..');
        await Audio.requestPermissionsAsync();
        await Audio.setAudioModeAsync({
          allowsRecordingIOS: true,
          playsInSilentModeIOS: true,
        });
  
        console.log('Starting recording..');
        const { recording } = await Audio.Recording.createAsync( Audio.RecordingOptionsPresets.HIGH_QUALITY
        );
        setRecording(recording);
        console.log('Recording started');
      } catch (err) {
        console.error('Failed to start recording', err);
      }
    }
  
    async function stopRecording() {
      console.log('Stopping recording..');
      setRecording(undefined);
      await recording.stopAndUnloadAsync();
      await Audio.setAudioModeAsync(
        {
          allowsRecordingIOS: false,
        }
      );
      const uri = recording.getURI();
      console.log('Recording stopped and stored at', uri);
    }
  

    // Taking permissions for camera/media library usage
    useEffect(() => {
        (async () => {
            const cameraPermission = await Camera.requestCameraPermissionsAsync();
            const mediaLibraryPermission = await MediaLibrary.requestPermissionsAsync;
            setHasCameraPermission(cameraPermission.status === "granted");
            setHasMediaLibraryPermission(mediaLibraryPermission.status === "granted");
        })();
    }, []);

    // Checking for camera permissions
    if (hasCameraPermission === undefined) {
        return <Text>Requesting permissions...</Text>
    } else if (!hasCameraPermission) {
        return <Text>Permission for camera not granted. Please change this in settings.</Text>
    }

    // Camera component
    return (
        <Camera style={styles.container}>
            <FAB
            icon="menu"
            style={styles.fab}
            onPress={() => navigation.navigate('Settings')}
            />
            <Button
        title={recording ? 'Stop Recording' : 'Start Recording'}
        onPress={recording ? stopRecording : startRecording}
      />
            <Text>Future implementation of Toast.</Text>
            <StatusBar style = "auto" />
        </Camera>
    );

}


const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    fab: {
        alignSelf: 'flex-start',
        left: 20,
        top: 0,
        marginBottom: 650,
        opacity: '1',
      },
  });