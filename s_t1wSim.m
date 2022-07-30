%% Qiyuan Tian 2022
clear, clc, close all

dpRoot = fileparts(which('s_t1wSim.m'));
dpData = fullfile(dpRoot, 'data');
dpSim = fullfile(dpRoot, 'data-sim');
mkdir(dpSim);

%% file pre
files = dir(fullfile(dpData, 'hcp*'))';

%% add noise
for ii = 1 : length(files)
    
    fnFile = files(ii).name;
    fpFile = fullfile(dpData, fnFile);
    
    tmp = load(fpFile);
    t1w = tmp.t1w;
    mask = tmp.mask; % find area of interesting
    maskdil = tmp.mask_dilate;
    
    %%% simulate low snr data
    t1wnorm = (t1w - mean(t1w(mask))) / std(t1w(mask)); % standardize image intensity to [-3 3]
    pd = makedist('Normal', 'mu', 0, 'sigma', 0.4); % add gaussian noise, 0 mean, 0.4 std dev
    noisesim = random(pd, size(t1w));            
    t1wnorm_lowsnr = t1wnorm + noisesim;
    t1w_lowsnr = t1wnorm_lowsnr * std(t1w(mask)) + mean(t1w(mask));
    t1w_lowsnr = t1w_lowsnr .* maskdil;

    figure, imshow(t1w(:, :, 100), [0, 1200]);
    figure, imshow(t1w_lowsnr(:, :, 100), [0, 1200]);
    figure, imshow(t1w(:, :, 100) - t1w_lowsnr(:, :, 100), [-500, 500]);

    
    %%% save data
    fnSave = [fnFile(1 : end - 4) '_sim.mat'];
    fpSave = fullfile(dpSim, fnSave);
    save(fpSave, 't1w_lowsnr');
end   


