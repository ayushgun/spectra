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
import { theme } from '../core/theme';



export default function Video({navigation}) {
    let cameraRef = useRef();
    const [hasCameraPermission, setHasCameraPermission] = useState();
    const [hasMediaLibraryPermission, setHasMediaLibraryPermission] = useState();


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
        opacity: 1,
      },
  });